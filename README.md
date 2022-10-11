# Python WordPress Export Parser

A Python module for parsing a WordPress XML export/backup into Python objects.
Useful for storing the data in some other form like a JSON file, or loading it into the database of a Python website project like a Django project.

## Installation

Download this Python file and drop it in your current project or somewhere on your Python path.

## Usage

```py
>>> import wordpress
>>> wp = wordpress.WordPress("path/to/wordpress/file.xml")
```
