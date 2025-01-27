# Julia

We maintain Julia modules (`module load exfel julia`) to set appropriate
environment variables, and a global read-only Julia depot.

## Updating Julia

[juliaup](https://github.com/JuliaLang/juliaup) is installed in the `xsoft`
account, and it's configured to store everything under
`/gpfs/exfel/sw/software/juliaup`.

- To update all installed Julia versions run `juliaup up`. Afterwards you will
  need to update the binary paths in the module files. Run `juliaup st` to see
  all installed versions.
- If a new minor version is available you may need to add the channel explicitly
  with `juliaup add 1.XX`, and then add a new modulefile for the new minor
  version. You will also need to add a cron job to update the global depot for
  the previous minor version (see the [global depot
  section](#the-global-depot)).

Currently we only maintain modules for minor versions, not patch versions. If it
turns out a specific patch version is necessary then we will need to rethink
this.

## The global depot and environments

The global depot is stored here: `/gpfs/exfel/sw/software/julia-depot`. It and
the global environments are updated automatically by cron jobs that run the
`update-julia-env` script (under `scripts/julia` of this repo). The Julia
modules will add the global depot to `JULIA_DEPOT_PATH` with the goal of
reducing precompilation times for users using those packages. A default Julia
environment is not activated by default but the latest one can be set with the
`JULIA_EXFEL_ENV` environment variable: `julia --project=$JULIA_EXFEL_ENV`.

The `Project.toml` and `Manifest-v*.toml` files of the environments are stored
in the `environments/` subdirectories along with the Python environment
lockfiles.

[CUDA.jl](https://cuda.juliagpu.org/stable/) is one of the packages we keep in
the environment and that must be precompiled on a GPU to work, so if you're
running `update-julia-depot` manually make sure you do it with e.g. `srun -p
allgpu update-julia-depot`. The cron jobs do that already. From time to time the
CUDA runtime should also be updated, to do that change the call to
`CUDA.set_runtime_version!` in the `update-julia-env` script.

- Run `crontab -e` as `xsoft` on `max-exfl-display001` to see the cron jobs for
  it. The precompile files are per-Julia version (and also a lot of other
  things that we don't care about), so there should be one cron job per
  supported Julia module.
- To add a package to an environment, activate the environment and `] add` it as
  usual. Remember to set a compat bound for it.
