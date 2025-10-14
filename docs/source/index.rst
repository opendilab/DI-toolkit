Welcome to DI-toolkit's Documentation
=========================================================

Overview
-------------

``DI-toolkit`` is a fundamental utility library within the OpenDILab ecosystem, designed to provide stable and efficient foundational support for other repositories in OpenDILab. It not only parses and manages the structure and versions of configuration files but also offers a range of practical tools to simplify common tasks such as distributed training, log management, and TensorBoard data processing, thereby accelerating the process of deep reinforcement learning research and development.

The design philosophy of this library is to provide modular and reusable components, reducing redundant efforts and ensuring consistency across OpenDILab projects. By abstracting underlying complexities, ``DI-toolkit`` enables developers to focus more on algorithmic innovation rather than infrastructure setup.

Key Features
-----------------

``DI-toolkit`` provides the following core functional modules to meet common requirements in deep reinforcement learning projects:

*   **Config Management**: Powerful configuration file parsing and management capabilities, supporting structured definition, version control, and dynamic loading of configuration files, ensuring flexibility and traceability in experimental configurations.
*   **Distributed Training Utilities**: Offers a series of convenient helper functions for PyTorch distributed training, including distributed environment detection, process-level information retrieval (such as rank and world size), and master process determination, greatly simplifying the writing and debugging of distributed training code.
*   **Logging System**: Provides a feature-rich logging solution, supporting terminal output, file output, and custom loggers, helping developers efficiently track and debug model training processes.
*   **TensorBoard Data Processing**: Includes tools for extracting and processing log data from TensorBoard event files, particularly scalar data, making it easier for users to analyze and visualize experimental results.

.. toctree::
    :maxdepth: 2
    :caption: Tutorials

    tutorials/installation/index
    tutorials/quick_start/index

.. toctree::
    :maxdepth: 2
    :caption: Best Practice


.. toctree::
    :maxdepth: 2
    :caption: API Documentation

    api_doc/config/index
    api_doc/distributed/index
    api_doc/logging/index

.. toctree::
    :maxdepth: 2
    :caption: Contributor Guide

