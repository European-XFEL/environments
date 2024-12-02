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

## The global depot

The global depot is stored here: `/gpfs/exfel/sw/software/julia-depot`. It's
updated automatically by cron jobs that run the `update-julia-depot` script
(under `scripts/julia` of this repo). The Julia modules will add the global
depot to `JULIA_DEPOT_PATH` with the goal of reducing precompilation times for
users using those packages.

[CUDA.jl](https://cuda.juliagpu.org/stable/) is one of the packages we keep in
the depot and that must be precompiled on a GPU to work, so if you're running
`update-julia-depot` manually make sure you do it with e.g. `srun -p allgpu
update-julia-depot`. The cron jobs do that already.

- Run `crontab -e` as `xsoft` on `max-exfl-display001` to see the cron jobs for
  it. The precompile files are per-Julia version (and also a lot of other
  things that we don't care about), so there should be one cron job per
  supported Julia module.
- To add a package to the depot just add it to the `packages` array in the
  script and it will be installed the next time the script is run.
