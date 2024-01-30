# CI/CD

## Documentation

The documentation is hosted with GitHub Pages, configured to deploy the contents of the `gh-pages` branch as a statically hosted web page.

There are two main workflows that are used to update the documentation:

1. `.github/workflows/docs.yml` - triggered on pushes to `main`, this will build the static site and push it to the `gh-pages` branch.
2. `.github/workflows/docs-pr.yml` - triggered on pull requests, this will build the static site, add it to a subdirectory `pr/<PR_NUMBER>`, and comment on the PR with a link to the preview. When the PR is closed, the directory is deleted.
3. `.github/workflows/docs-pr-cleanup.yml` - triggered on pull request close or merge, this will delete the preview directory.

### EuXFEL User Documentation Integration

The user documentation is hosted on EuXFEL RTD, it is 'integrated' with the environments documentation by including this repository as a submodule, which is then built as part of the user documentation build process.

To keep the two in sync, when the documentation is updated (merge/push to `main`) it triggers a RTD webhook to rebuild the user documentation, which will pull the latest version of the submodule.

For more information see:

- <https://github.com/European-XFEL/environments/pull/24>
- <https://git.xfel.eu/dataAnalysis/user-documentation/-/merge_requests/107>

## Package Builds

!!! warning "Work in Progress"

    Some work done in:

    - https://github.com/European-XFEL/environments/pull/30
    - https://github.com/European-XFEL/environments/tree/feat/build-pkg-ci

## Environment Builds

!!! warning "Work in Progress"
