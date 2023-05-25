import os
import shutil
from enum import IntEnum, Enum

from yattag import Doc

from ditk import logging

code_js = r"""
window.onload = function(){
    var codeElement = document.getElementsByName('py_code');
    var lineCount = 1;
    for (var i = 0; i < codeElement.length; i++) {
        var code = codeElement[i].innerText;
        if (code.length <= 1) {
            continue;
        }

        codeElement[i].innerHTML = "";

        var codeMirror = CodeMirror(
          codeElement[i],
          {
            value: code,
            mode: "python",
            theme: "solarized dark",
            lineNumbers: true,
            firstLineNumber: lineCount,
            readOnly: false,
            lineWrapping: true,
          }
        );
        var noNewLineCode = code.replace(/[\r\n]/g, "");
        lineCount += code.length - noNewLineCode.length + 1;
    }
};
"""


class StateCode(IntEnum):
    NORMAL = 0
    LINE_COMMENT = 1
    BLOCK_COMMENT = 2


class Lang(str, Enum):
    Chinese = 'zh'
    English = 'en'


def _get_assets(path, *paths):
    return os.path.normpath(os.path.join(__file__, '..', path, *paths))


def generate_annotated_doc(src_py_path, dst_html_path, title,
                           ds_assets_path=None, lang: Lang = Lang.English):
    if not ds_assets_path:
        ds_assets_path = os.path.normcase(os.path.normpath(os.path.join(dst_html_path, '..', 'assets')))
    ds_assets_path = os.path.abspath(ds_assets_path)
    dst_html_dir = os.path.dirname(os.path.abspath(dst_html_path))
    if not os.path.exists(ds_assets_path):
        os.makedirs(ds_assets_path, exist_ok=True)

    def _get_rel_url_from_html(asset_path):
        segments = os.path.relpath(asset_path, start=dst_html_dir).split(os.path.sep)
        return '/'.join(segments)

    def _place_asset(path, *paths):
        segments = [path, *paths]
        dst_file = os.path.join(ds_assets_path, segments[-1])
        shutil.copyfile(_get_assets(*segments), dst_file)
        return _get_rel_url_from_html(dst_file)

    with open(src_py_path, 'r') as f:
        src = f.read()
    line_data = src.split('\n')
    doc, tag, text, line = Doc().ttl()
    with tag('html'):
        with tag('head'):
            with tag('meta', charset="utf-8"):
                pass
            with tag('title'):
                text(title)
            with tag('link', rel="stylesheet", href=_place_asset('pylit.css')):
                pass
            with tag('link', rel="stylesheet", href=_place_asset('solarized.css')):
                pass
            with tag('link', rel="stylesheet", href="https://cdn.jsdelivr.net/npm/katex@0.16.3/dist/katex.min.css",
                     integrity="sha384-Juol1FqnotbkyZUT5Z7gUPjQ9gzlwCENvUZTpQBAPxtusdwFLRy382PSDx5UUJ4/",
                     crossorigin="anonymous"):
                pass
            with tag('script', src="https://cdn.jsdelivr.net/npm/katex@0.16.3/dist/katex.min.js",
                     integrity="sha384-97gW6UIJxnlKemYavrqDHSX3SiygeOwIZhwyOKRfSaf0JWKRVj9hLASHgFTzT+0O",
                     crossorigin="anonymous"):
                pass
            with tag('script', src="https://cdn.jsdelivr.net/npm/katex@0.16.3/dist/contrib/auto-render.min.js",
                     integrity="sha384-+VBxd3r6XgURycqtZ117nYw44OOcIax56Z4dCRWbxyPt0Koah1uHoK0o4+/RRE05",
                     crossorigin="anonymous", onload="renderMathInElement(document.body);", defer=True):
                pass
            with tag('link', rel="stylesheet",
                     href="https://cdn.jsdelivr.net/npm/codemirror@5.61.0/lib/codemirror.min.css"):
                pass
            with tag('script'):
                doc.attr(src="https://cdn.jsdelivr.net/npm/codemirror@5.61.0/lib/codemirror.min.js")
            with tag('script'):
                doc.attr(src="https://cdn.jsdelivr.net/npm/codemirror@5.61.0/mode/python/python.min.js")

        with tag('body'):
            def item_fn(doc_data, code_data, cnt):
                if len(doc_data) == 0:
                    return
                doc_data = doc_data.replace('\n', '<br>')
                doc_data = doc_data.replace('**:', '</b>')
                doc_data = doc_data.replace('**', '<b>')
                doc_data = doc_data.replace(' ``', ' <span style="color:#00cbf694;font-family:Monaco,IBMPlexMono;">')
                doc_data = doc_data.replace('`` ', '</span> ')
                doc_data = doc_data.replace('<link ', '<a href="')
                doc_data = doc_data.replace(' link>', '">Related Link</a>')
                with tag('div', klass='section', id=f'section-{cnt}'):
                    if cnt == 0:
                        with tag('div', klass='docs doc-strings'):
                            with tag('p'):
                                with tag('p'):
                                    with tag('a', href='index.html'):
                                        with tag('b'):
                                            text("HOME<br>")

                            with tag('a', href="https://github.com/opendilab/PPOxFamily", target="_blank"):
                                with tag('img', alt="GitHub", style="max-width:100%;"):
                                    doc.attr(
                                        src="https://img.shields.io/github/stars/opendilab/PPOxFamily?style=social"
                                    )
                            text('  ')
                            with tag('a', href="https://space.bilibili.com/1112854351?spm_id_from=333.337.0.0",
                                     target="_blank"):
                                with tag('img', alt="bilibili", style="max-width:100%;"):
                                    doc.attr(src="https://img.shields.io/badge/bilibili-video%20course-blue")
                            text('  ')
                            with tag('a', href="https://twitter.com/OpenDILab", rel="nofollow", target="_blank"):
                                with tag('img', alt="twitter", style="max-width:100%;"):
                                    doc.attr(src="https://img.shields.io/twitter/follow/opendilab?style=social")
                            text('<br>')
                            with tag('a',
                                     href=f"https://github.com/opendilab/PPOxFamily/tree/main/{src_py_path}",
                                     target="_blank"):
                                text("View code on GitHub")
                            text('<br><br>')
                            text(doc_data)

                    else:
                        with tag('div', klass='docs doc-strings'):
                            with tag('p'):
                                text(doc_data)

                        with tag('div', klass='code'):
                            with tag('pre'):
                                with tag('code', id=f"code_{cnt}", name="py_code"):
                                    text(code_data)

            cnt = 0
            state = StateCode.NORMAL
            line_code, line_comment, block_comment = [], [], []
            for i in range(len(line_data)):
                logging.info(f'{i:3d} {line_data[i]}')
                no_space_data = line_data[i].strip()
                if no_space_data.startswith('if __name__ == "__main__":'):
                    break
                if state == StateCode.NORMAL:
                    if no_space_data.startswith('"""'):  # block comment
                        state = StateCode.BLOCK_COMMENT
                    elif no_space_data.startswith('#'):  # line comment
                        item_fn('\n'.join(line_comment), '\n'.join(line_code), cnt)
                        line_code, line_comment, block_comment = [], [], []
                        cnt += 1
                        state = StateCode.LINE_COMMENT
                        line_comment.append(line_data[i].replace('# ', ''))  # remove '# '
                        if 'delimiter' in line_data[i]:
                            line_comment[-1] = ''
                    else:
                        line_code.append(line_data[i])
                elif state == StateCode.LINE_COMMENT:
                    if no_space_data.startswith('#'):
                        line_comment.append(line_data[i].replace('# ', ''))  # remove '# '
                    else:
                        state = StateCode.NORMAL
                        line_code.append(line_data[i])
                elif state == StateCode.BLOCK_COMMENT:
                    if no_space_data.startswith('"""'):  # block comment end
                        item_fn('\n'.join(block_comment), '\n'.join(line_code), cnt)
                        line_code, line_comment, block_comment = [], [], []
                        cnt += 1
                        state = StateCode.NORMAL
                    else:
                        block_comment.append(line_data[i])
                else:
                    raise RuntimeError(state)

            item_fn('\n'.join(line_comment), '\n'.join(line_code), cnt)
            with tag('div', klass='section', id=f'section-{cnt}'):
                with tag('div', klass='docs doc-strings'):
                    with tag('p'):
                        with tag('i'):
                            if lang == Lang.Chinese:
                                text('如果读者关于本文档有任何问题和建议，可以在 GitHub 提 issue 或是直接发邮件给我们'
                                     ' (opendilab@pjlab.org.cn) 。')
                            elif lang == Lang.English:
                                text(
                                    'If you have any questions or advices about this documentation, '
                                    'you can raise issues in GitHub (https://github.com/opendilab/PPOxFamily) '
                                    'or email us (opendilab@pjlab.org.cn).'
                                )
                            else:
                                raise ValueError(f'Unsupported lang - {lang!r}.')

        with tag('script', type="text/javascript"):
            text(code_js)

    result = doc.getvalue()
    result = result.replace('&lt;', '<')
    result = result.replace('&gt;', '>')
    with open(dst_html_path, 'w') as f:
        f.write('<!DOCTYPE html>\n' + result)

    logging.info(f'[green]Log to [u]{dst_html_path}[/u] success![/green]')


if __name__ == "__main__":
    generate_annotated_doc('ppo.py', 'ppo.html', 'This is the title')
