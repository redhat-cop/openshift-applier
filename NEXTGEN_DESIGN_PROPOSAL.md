# Design Proposal for Project "Dash"

The openshift-applier has done well in its current shape as an ansible playbook paired with an inventory, driving what content to seed an openshift-cluster with. However, it also has some flaws that now can be better addressed with newer technologies and approaches that are becoming mainstream. This document captures the proposed design of the next iteration of this project, with new branding and a new contract.

The working name for the project is "Dash" (because when you remove the words `openshift` and `applier`, you're left with `-`).

## Design Philosophy

Dash has a goal of becoming THE automation framework for Kubernetes. In order to acheive this, we feel that we must adhere to a set of principles for how Kubernetes automation should be done.

- One should represent all Kubernetes resource definitions in files, or templates and parameters that produce files. This is in line with the the strategy for [Declarative Management of Kubernetes Objects](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/declarative-config/)
- These definition files should be version controlled in Git.
- Once resource definitions are defined as files in a repository, they should be reconciled to the Kubernetes API using repeatable raw verbs. This means:
  - `kubectl apply` should be the default, and used for all resources whose full lifecycle will be managed.
  - `kubectl patch` should be used for files where we only manage certain fields.
  - `kubectl create` or `kubectl replace` should be used sparingly, being used only where there are immutable fields to contend with that `apply` would not work on.
    - If using `create` the automation should gracefully handle `Already Exists` errors, taking no action and allowing the automation to continue.
  - `kubectl delete` may be used to remove resources that are provisioned in the cluster by default, but not desired.
    - If using `delete` the automation should gracefully handle `Does Not Exist` errors, taking no action and allowing the automation to continue.
- Every entity that has a set of resources to manage, be it a person, team, or robot, should manage its own repository of resource files.
- In some cases the configuration of a resource may depend on values of fields in other resources in the cluster. The automation should provide a way to handle this through a _discovery model_, allowing to do `get` calls to retrieve values that can be used as template parameters later in the run.
- Processing of templates should be done client-side, so as to keep the automation portable across any cluster. This also allows for batching of POST/PUT calls to the API server.

## Desired Feature List

The following is a list of features we would like to see in Dash. This is not intended to represent a _Minimum Viable Product_, but a long term list of desired features. From here we will define a subset that defines our MVP.

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
- For very simple use cases, Dash should not _require_ an inventory file.
  - In order to lower the barrier, Dash should be able to run against an embedded default inventory such that simple repositories with a predictable directory structure could run without its own inventory file.
  - (see below for proposed default values)

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

A _default_ Dash inventory.

```
verison: 3.0
resource_groups:
  - name: Default Resources
    resources:
    - name: Raw Manifests
      file: manifests/
    - name: Helm Templates
      template: helm/
      type: helm
    - name: OpenShift Templates
      template: openshift-templates/
      params: openshift-template-params/
```
