# Design Proposal for Project "Dash"

The openshift-applier has done well in its current shape as an ansible playbook paired with an inventory, driving what content to seed an openshift-cluster with. However, it also has some flaws that now can be better addressed with newer technologies and approaches that are becoming mainstream. This document captures the proposed design of the next iteration of this project, with new branding and a new contract.

The working name for the project is "Dash" (because when you remove the words `openshift` and `applier`, you're left with `-`).

## Design Philosophy

TODO

## Desired Feature List

- Dash should be written in Golang to align with other projects in the Kubernetes ecosystem.
- Dash should take the form of a CLI tool, and an API library that could be directly consumed by other projects
- Dash should not be “object aware” and hence not process any kubernetes/openshift objects itself (just as the current openshift-applier works)
  - This avoids the ties to a specific version of kubernetes / OpenShift objects
- Dash should re-use the same “inventory” format as the previous openshift-applier, making it easier for existing users to adapt Dash
  - Newer versions are ok, but it should handle existing inventories for backwards compatibility
- Dash should support filter capabilities to only apply a portion of the inventories
- Dash should support dynamically combining multiple “inventory” definitions to compose a bigger collection of objects
  - Making it possible to re-use the same definitions more easily to avoid duplicates
- Dash should support source its inventory content URLs and local files + input parameters from the supplied inventory (mimic the current openshift-applier)
- Dash should be capable of handling “deltas” and only process changes on consecutive runs if desired (controlled by flags)
  - Could be based on commit id or other ways of capturing “the diff”
- Dash should support multiple template processing mechanisms in a pluggable format including:
  - Helm
  - Kustomize
  - OpenShift Templates
  - some freeform templating system, like Jinja2
- Dash should support pre/post hooks to for example “post-process” aspects like service/application configuration and “pre-process” waiting for resources to be available
- Consider capturing metrics around Dash usage and show in cluster dashboards (i.e.: use prometheus to capture data to show in a grafana dashboard).
- Dash should be able to process content that is behind a private endpoint (URL,repo,etc.)
- Dash should support all basic kubernetes API verbs, including:
  - Apply
  - Create
  - Replace
  - Delete
  - Exec
  - Get
  - Patch
- Dash should support runs across Multiple Kubernetes clusters
- Dash should support variable hierarchy, such that variables can be set at multiple levels, overriding as they get more specific.

# Working Inventory Contract

The Dash _inventory_ will be the file where users define what contents exist and how they should be handled.

```
# .dash.yml

version: <2.0|3.0> # This is how we will maintain backwards compatibility. A value of '2.0' will run the current `openshift-applier`

context: global-context #if not specified, should default to the current active context or fail right away if one is not able to be identified.
namespace: global-default
resource_groups: # This will replace `object` in openshift-applier, and serve as a logical grouping of content. This will be the level at which we pre-process all template content before putting to the api. Resource_groups should be able to be parent/child of other resource groups.
  - name: Group 1 # name fields are not required, just used for logging/debugging
    namespace: group1-stuff
    resources:
      - name: A Deployment
        namespace: this-deployment
        type: <manifest|helm|openshift|kustomize>
        template:
        params:
# Group 1 would run a deployment to the group1-stuff namespace using the global-context kube-context and apply a template using a specific set of params
  - name: Group 2
    resources:
      - name: Another Deployment
        type: <manifest|helm|openshift|kustomize>
        file:
        context: a-different-kube-context
# Group 2 would run a deployment to the global-default namespace using the a-different-kube-context kube-context and process a standard file (i.e. not a template)
```
