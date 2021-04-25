# Python implementation of AbstractMark.
For more information about Abstractmark, please visit this [repository](https://github.com/abstractmark/abstractmark).

## Requirement
- Python Version >= 3.9

## CLI
- Usage:
    - For Converting Abstractmark file: run `python3 abstractmark [abstractmark file] [abstractmark options] [args]`
    - For Converting Abstractmark files inside a folder: run `python3 abstractmark [folder] [abstractmark options args]`
    - For Abstractmark's Information : run `python3 abstractmark [option]`
    - For more information about AbstractMark CLI, please type `abstractmark --help` on your terminal.

## Import AbstractMark
- Usage:
    - `from abstractmark import AbstractMark` to import AbstractMark
    - Pass your text to convert into AbstractMark class with your options and use `convert` function to convert it, example: `AbstractMark("# Hello World {#Hi} {color:red}", styled = False).convert()`

- Available options:
    - `styled`, convert your text into html tags with default styled
    - `fullHTMLTags`, convert your text into full structured html tags.

## Code of Conduct
For the Code of Conduct, please visit [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## Contributing Guidelines
Thanks for your interest in contributing to AbstractMark! Please take a moment to review this [document](CONTRIBUTING.md)

## License
AbstractMark is distributed under [MIT License](LICENSE)
