"""
PyTorch's implementation of Proximal Policy Optimization (PPO)
"""
from collections import namedtuple
from typing import Optional, Tuple

import torch

ppo_policy_data = namedtuple('ppo_policy_data', ['logit_new', 'logit_old', 'action', 'adv', 'weight'])
ppo_policy_loss = namedtuple('ppo_policy_loss', ['policy_loss', 'entropy_loss'])
ppo_info = namedtuple('ppo_info', ['approx_kl', 'clipfrac'])


def ppo_policy_error(data: namedtuple,
                     clip_ratio: float = 0.2,
                     dual_clip: Optional[float] = None) -> Tuple[namedtuple, namedtuple]:
    """
    **Overview**:
        Implementation of Proximal Policy Optimization <link https://arxiv.org/pdf/1707.06347.pdf link>
        with entropy bounus, value_clip and dual_clip.
    """
    # Unpack data: $$<\pi_{new}(a|s), \pi_{old}(a|s), a, A^{\pi_{old}}(s, a), w>$$
    logit_new, logit_old, action, adv, weight = data
    # Prepare weight for default cases.
    if weight is None:
        weight = torch.ones_like(adv)
    # Prepare policy distribution from logit and get log propability.
    dist_new = torch.distributions.categorical.Categorical(logits=logit_new)
    dist_old = torch.distributions.categorical.Categorical(logits=logit_old)
    logp_new = dist_new.log_prob(action)
    logp_old = dist_old.log_prob(action)
    # Entropy bonus: $$\pi_{new}(a|s) log(\pi_{new}(a|s))$$
    dist_new_entropy = dist_new.entropy()
    entropy_loss = (dist_new_entropy * weight).mean()
    # Importance sampling weight: $$r(\theta) = \frac{\pi_{new}(a|s)}{\pi_{old}(a|s)}$$
    ratio = torch.exp(logp_new - logp_old)
    # Original surrogate objective: $$r(\theta) A^{\pi_{old}}(s, a)$$
    surr1 = ratio * adv
    # <b>Clipped surrogate objective:</b> $$clip(r(\theta), 1-\epsilon, 1+\epsilon) A^{\pi_{old}}(s, a)$$
    surr2 = ratio.clamp(1 - clip_ratio, 1 + clip_ratio) * adv
    # Dual clip proposed by <link https://arxiv.org/abs/1912.09729 link> .
    # Only use dual_clip when adv < 0.
    if dual_clip is not None:
        clip1 = torch.min(surr1, surr2)
        clip2 = torch.max(clip1, dual_clip * adv)
        policy_loss = -(torch.where(adv < 0, clip2, clip1) * weight).mean()
    # PPO-Clipped Loss: $$min(r(\theta) A^{\pi_{old}}(s, a), clip(r(\theta), 1-\epsilon, 1+\epsilon) A^{\pi_{old}}(s, a))$$
    # Multiply sample-wise weight and reduce mean in batch dimension.
    else:
        policy_loss = (-torch.min(surr1, surr2) * weight).mean()
    # Add some visualization metrics to monitor optimization status.
    with torch.no_grad():
        approx_kl = (logp_old - logp_new).mean().item()
        clipped = ratio.gt(1 + clip_ratio) | ratio.lt(1 - clip_ratio)
        clipfrac = torch.as_tensor(clipped).float().mean().item()
    # Return final loss and information.
    return ppo_policy_loss(policy_loss, entropy_loss), ppo_info(approx_kl, clipfrac)
