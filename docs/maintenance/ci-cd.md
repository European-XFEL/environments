# CI/CD

## Documentation

The documentation is hosted with GitHub Pages, configured to deploy the contents of the `gh-pages` branch as a statically hosted web page.

There are two main workflows that are used to update the documentation:

1. `.github/workflows/docs.yml` - triggered on pushes to `main`, this will build the static site and push it to the `gh-pages` branch.
2. `.github/workflows/docs-pr.yml` - triggered on pull requests, this will build the static site, add it to a subdirectory `pr/<PR_NUMBER>`, and comment on the PR with a link to the preview. When the PR is closed, the directory is deleted.
