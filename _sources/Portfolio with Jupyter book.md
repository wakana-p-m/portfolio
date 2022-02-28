# Portfolio with Jupyter book

This portfolio site is made of [Jupyer Book](https://jupyterbook.org/intro.html). Jupyter book is an open-source project to build beautiful documentation.  

I looked for different options, but I decided to go with Jupter Book for the following reasons.
- Compatible with Python and R (Additional steps are required to convert R markdown files)
- I can publish Jupyter notebook directly
- No need to host a website
- Simple design that does not require a lot of customization 

## Setup
*Step 1.*  Install Jupyter Book
```
pip install -U jupyter-book
```

### Building a book
##### *Step 2.*  Create book content
https://jupyterbook.org/start/create.html
Using this sample book as a template.
`_config.yml`, `_toc.yml` and book content written in Jupyter Notebook (`.ipynb`) or MyST Markdown (`.md`), or reStructuredText(`.rst`).
```
$ jupyter-book create mynewbook/
```

##### *Step 3.*  Build book, meaning converting the content to HTML
Once your content are created, add the content files to the table of content. (`_toc.yml`).

```
$ tree mybookname
```
```
mybookname/
├── _config.yml
├── _toc.yml
├── intro.md
├── logo.png
├── markdown-notebooks.md
├── markdown.md
├── notebooks.ipynb
├── references.bib
└── requirements.txt
```
Then, build book's HTML.
```
jupyter-book build mybookname/
```

```{note}
By default, Jupyter Bokk will only build the HTML for pages that have been updated since the last time you build the book. To signal a full re-build, use `--all` option:
```
```
jupyter-book build --all mybookname/
```

##### *Step 4.* Publish book on line
The book will be published on GitHub pages, a free online hosting platform.
https://jupyterbook.org/start/publish.html

*For the first time*
1. Create a new repository on Github https://github.com/new
```{note}
Make the repository public and do not initialize it with a README file.
```
2. Close the (currently empty) online repository to your local computer.

*Whenever making changes to the content*
```
git clone https://github.com/<my-org>/<my-repository-name>
```
3. Copy all of the book files and fodler into the newly closed repository.
```
cp -r mylocalbook/* myonlinebook/
```
4. SYnc your local and online repositories
```
cd myonlinebook
git add ./*
git commit -m "adding my first book!"
git push
```

###### Publish the book
https://jupyterbook.org/start/publish.html
Now the source files have been pushed into GitHub repository. The next step it to make them publically accessible. Use `ghp-import` package, which makes it easy to push HTML conten to a GitHub repository.

*Just for the first time*
```
pip install ghp-import
```
*Use this code whenever publishing updates*
```
ghp-import -n -p -f _build/html
```

## Converting R Markdown to Jupyter Notebook
https://medium.datadriveninvestor.com/transforming-your-rmd-to-ipynb-file-r-markdown-to-python-jupyter-b1306646f50b
To a convert R markdown file to a jupyer notebook, we will use `rmd2jupyter`.
```{note}
It's important that run the Jupyter notebook that converted from R markdown on a environment that R language and essential pakages are installed.
https://docs.anaconda.com/anaconda/navigator/tutorials/r-lang/
````

*Just for the first time*
```
devtools::install_github("mkearney/rmd2jupyter")
library(rmd2jupyter)
```

```{note}
Install `devtools` r package if you don't have it yet.
https://devtools.r-lib.org/
```

*Convert a file*
```
rmd2jupyter("sample_file.Rmd")
```

Run the converted file on Jupyter notebook, select the R environment.

## Key Customization
### Hide code cell content/outputs or remove call inputs/outputs
Add metadata to Jupyter notebook to hide or remove code cell content/outputs.
https://jupyterbook.org/content/metadata.html#jupyter-cell-tags
1. To enable the cell tag editor, click `View -> Cell Toolbar ->` on Jupyter norbook.
2. Click "Edit Metadata" on cell that you want to control the behavior of Jupyter book

#### Hide code cell content
##### Hide cell inputs
```
{
    "tags": [
        "hide-input",
    ]
}
```
##### Hide cell outputs
```
{
    "tags": [
        "hide-output"
    ]
}
```
##### Hide entire cells
```
{
    "tags": [
        "hide-cell"
    ]
}
```
#### Remove code cell content
##### Remove cell imputs
```
{
    "tags": [
        "remove-output"
    ]
}
```
##### Remove cell outputs
```
{
    "tags": [
        "remove-cell"
    ]
}
```
##### Remove an entire code cell
You don’t need to do anything to remove empty cells from your pages. Jupyter Book will remove these automatically. 

