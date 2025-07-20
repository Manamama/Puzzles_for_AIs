::: {#hero-spot .section .hero-spot}
[![GitHub Pages](/images/logo.svg){.logo}](/)

Websites for you and your projects.
===================================

Hosted directly from your [GitHub repository](https://github.com). Just edit, push, and your changes are live.
--------------------------------------------------------------------------------------------------------------

[Pages Help](https://help.github.com/pages/){.help-link}

::: {#slideshow}
![Bootstrap](/images/slideshow/bootstrap.png){.slide .active
width="893"}
:::
:::

::: {#tutorial .section .tutorial}
Ready to get started? Build your own site from scratch or generate one for your project.
========================================================================================

You get one site per GitHub account and organization, and unlimited project sites. Let's get started.
-----------------------------------------------------------------------------------------------------

-   [User or organization site](#user-site){.selected}
-   [Project site](#project-site)

#### Create a repository

Head over to [GitHub](https://github.com) and [create a new public
repository](https://github.com/new) named *username*.github.io, where
*username* is your username (or organization name) on GitHub.

If the first part of the repository doesn't exactly match your username,
it won't work, so make sure to get it right.

#### What git client are you using?

-   [A terminal](#terminal-step-1){#option-terminal .selected}
-   [GitHub Desktop](#setup-in-desktop){#option-desktop}
-   [I don\'t know](#new-user-step-1){#option-newuser}

#### Download GitHub Desktop

GitHub Desktop is a great way to use Git and GitHub on macOS and
Windows.

[[]{.icon}Download GitHub
Desktop](https://desktop.github.com){.desktop-download} ![GitHub Desktop
screenshot](images/dashboard@2x.png){.full-size width="1054"}

#### Clone the repository

Go to the folder where you want to store your project, and clone the new
repository:

::: {.terminal}
::: {.header}
:::

::: {.shell}
[\~]{.path}[\$]{.prompt}git clone
https://github.com/*username*/*username*.github.io
:::
:::

#### Clone the repository

Click the \"Set up in Desktop\" button. When the GitHub desktop app
opens, save the project.

If the app doesn\'t open, launch it and clone the repository from the
app.

#### Clone the repository

After finishing the installation, head back to GitHub.com and refresh
the page. Click the \"Set up in Desktop\" button. When the GitHub
desktop app opens, save the project.

If the app doesn\'t open, launch it and clone the repository from the
app.

#### Hello World

Enter the project folder and add an index.html file:

::: {.terminal}
::: {.header}
:::

::: {.shell}
[\~]{.path}[\$]{.prompt}cd *username*.github.io

[\~]{.path}[\$]{.prompt}echo \"Hello World\" \> index.html
:::
:::

#### Create an index file

Grab your favorite text editor and add an index.html file to your
project:

::: {.terminal}
::: {.header}
index.html
:::

`           `{.shell}

    <!DOCTYPE html>
    <html>
    <body>
    <h1>Hello World</h1>
    <p>I'm hosted with GitHub Pages.</p>
    </body>
    </html>

#### Push it

Add, commit, and push your changes:

::: {.terminal}
::: {.header}
:::

::: {.shell}
[\~]{.path}[\$]{.prompt}git add \--all

[\~]{.path}[\$]{.prompt}git commit -m \"Initial commit\"

[\~]{.path}[\$]{.prompt}git push -u origin main
:::
:::

#### Commit & publish

Enter the repository, commit your changes, and press the publish button.

![Demonstration of steps required to create the initial commit and
publish the repository in GitHub
Desktop](images/desktop-demo@2x.gif){.macos-drop-shadow width="841"}

#### ...and you\'re done!

Fire up a browser and go to **https://*username*.github.io**.

::: {.hero-octicon}
[]{.mega-octicon .octicon-check}
:::

-   #### Use a theme, or start from scratch?

    You have the option to start with one of the pre-built themes,\
    or to create a site from scratch.

    -   [Choose a theme](#generate-step-1){#option-generate .selected}
    -   [Start from scratch](#vanilla-step-1){#option-vanilla}

-   ::: {#generate-step-1}
    #### Repository Settings

    Head over to [GitHub.com](https://github.com/) and create a new
    repository, or go to an existing one.\
    **Click on the Settings tab**.

    ![Settings for a
    repository](images/repo-settings@2x.png){width="720"}
    :::

-   #### Theme chooser

    Scroll down to the **GitHub Pages** section. Press **Choose a
    theme**.

    ![Automatic Generator button on GitHub.com,
    Settings](images/launch-theme-chooser@2x.png){width="720"}

-   #### Pick a theme

    Choose one of the themes from the carousel at the top.\
    When you\'re done, click **Select theme** on the right.

    ![Choose layout](images/theme-chooser@2x.png){.full-size
    width="720"}

-   #### Edit content

    Use the editor to add content to your site.

    ![Add content to your GitHub Pages
    site](images/code-editor@2x.png){.full-size width="720"}

-   #### Commit

    Enter a commit comment and click on **Commit changes** below the
    editor.

    ![Commit Markdown content to your
    repository](images/commit-edits@2x.png){.full-size width="720"}

-   ::: {#vanilla-step-1}
    #### Create an index file

    Head over to [GitHub.com](https://github.com/) and [create a new
    repository](https://github.com/new), or go to an existing one.\
    Click on the **Create new file** button.

    ![Create a file in your
    repository](images/new-create-file@2x.png){width="720"}
    :::

-   #### Hello World

    Name the file `index.html` and type some HTML content into the
    editor.

    ![Hello World on
    GitHub.com](images/new-index-html@2x.png){width="720"}

-   #### Commit the file

    Scroll to the bottom of the page, write a commit message, and commit
    the new file.

    ![Commit the file](images/new-commit-file@2x.png){width="720"}

-   #### Repository Settings

    **Click on the Settings tab** and scroll down to the GitHub Pages
    section.\
    Then select the **main branch** source and click on the **Save**
    button.

    ![GitHub Pages Source
    Setting](images/source-setting@2x.png){width="720"}

-   #### ...and you\'re done!

    Fire up a browser and go to
    **http://*username*.github.io/*repository***.

    ::: {.hero-octicon}
    []{.mega-octicon .octicon-check}
    :::

::: {#next-steps .section}
Now that you're up and running, here are a few things you should know.
======================================================================

-   [[]{.mega-octicon
    .octicon-pencil}](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll){.hero-octicon}

    #### [Blogging with Jekyll](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll)

    Using [Jekyll](https://jekyllrb.com), you can blog using beautiful
    Markdown syntax, and without having to deal with any databases.
    [Learn how to set up Jekyll](https://jekyllrb.com/docs/).

-   [[]{.mega-octicon
    .octicon-link}](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site){.hero-octicon}

    #### [Custom URLs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

    Want to use your own custom domain for a GitHub Pages site? Just
    create a file named CNAME and include your URL. [Read
    more](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site).

-   [[]{.mega-octicon
    .octicon-book}](https://docs.github.com/pages){.hero-octicon}

    #### [Guides](https://docs.github.com/pages)

    Learn how to create custom 404 pages, use submodules, and [learn
    more about GitHub Pages](https://docs.github.com/pages).
:::

-   [Status](https://www.githubstatus.com/)
-   [API](https://docs.github.com/rest)
-   [Training](https://training.github.com)
-   [Shop](https://shop.github.com)
-   [Blog](https://github.blog)
-   [About](https://github.com/about)

[[]{.mega-octicon .octicon-mark-github}](/)

-   © 2025 GitHub, Inc.
-   [Terms](https://docs.github.com/en/github/site-policy/github-terms-of-service)
-   [Privacy](https://docs.github.com/en/github/site-policy/github-privacy-statement)
-   [Security](https://github.com/security)
-   [Contact](https://support.github.com)
:::
:::
