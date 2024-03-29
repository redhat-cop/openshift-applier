# openshift-applier

Role used to apply OpenShift objects to an existing OpenShift Cluster.

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [openshift-applier](#openshift-applier)
  - [Requirements](#requirements)
  - [Role Usage](#role-usage)
    - [Sourcing OpenShift Object Definitions](#sourcing-openshift-object-definitions)
    - [Template processing](#template-processing)
    - [Using oc vs kubectl](#using-oc-vs-kubectl)
    - [Sourcing a directory with files](#sourcing-a-directory-with-files)
    - [Ordering of Objects in the inventory](#ordering-of-objects-in-the-inventory)
    - [Privileged Objects](#privileged-objects)
    - [Object Entries in the Inventory](#object-entries-in-the-inventory)
    - [Override default actions with `action`](#override-default-actions-with-action)
    - [Passing extra arguments to the client](#passing-extra-arguments-to-the-client)
    - [Filtering content based on tags](#filtering-content-based-on-tags)
    - [Suppressing log output](#supressing-log-output)
    - [Pre/Post steps](#prepost-steps)
    - [Deprovisioning](#deprovisioning)
    - [Dependencies](#dependencies)
  - [Example Playbook](#example-playbook)
  - [License](#license)
  - [Author Information](#author-information)

<!-- /TOC -->


## Requirements

A working OpenShift or Kubernetes cluster that can be used to populate things like namespaces, policies and PVs (all require cluster-admin), or application level content (cluster-admin not required).


## Role Usage

### Sourcing OpenShift Object Definitions

The variable definitions come in the form of an object, `openshift_cluster_content`, which contains sub-objects containing file, template, and parameter definitions. At its simplest, this definition looks like this:

```yaml
openshift_cluster_content:
- galaxy_requirements: # Optional: only needed if pre/post steps are specified below
    - "path/to/galaxy/requirements.yml" # Has to be a local file - e.g: with the inventory
- galaxy_sources:      # Optional: only needed if pre/post steps are specified below
    - src: https://github.com/....
      version: v1.0.0
    - src: https://github.com/....
      version: main
- object: <object_type>
  pre_steps: # Optional: pre-steps at object level can be added if desired
    - role: <path to an ansible role>
  content:
  - name: <definition_name>
    pre_steps: # Optional: pre-steps at content level can be added if desired
      - role: <path to an ansible role>
        vars: # Optional: only needed if the role above needs values passed
          <key1>: <value1>  
    file: <file source>
    action: <apply|create> # Optional: Defaults to 'apply'
    no_log: <True|False> # Optional: no_log at content level if functionality desired. Defaults to False
    tags: # Optional: Tags are only needed if `include_tags` or `exclude_tags` is used
    - tag1
    - tag2
    post_steps: # Optional: post-steps at content level can be added if desired
      - role: <path to an ansible role>
  no_log: <True|False> # Optional: no_log at object level if functionality desired. Optional: Defaults to False
  post_steps: # Optional: post-steps at object level can be added if desired
    - role: <path to an ansible role>
- object: <object_type>
  content:
  - name: <definition_name>
    template: <template_source>
    action: <apply|create> # Optional: Defaults to 'apply'
    params: <params_file_source> # Optional if template has all default values for required fields
    params_from_vars: <params_dictionary_variable> # Optional: Use to supply additional run-time params or override params from file
    namespace: <target_openshift_namespace>
- object: <object_type>
  content:
  - name: <definition_name>
    helm:
      name: <helm chart name>  # Required
      action: <template|install> # Optional: defaults to 'template'
      chart: <helm chart source> # Required
      version: <chart version to use> # Optional
      namespace: <namespace scope> # Optional 
      repos: # Optional
      - name: repo1
        url: https://repo1.helm/...
      - name: repo2
        url: https://repo2.helm/...
      set_param: # Optional: List of "--set " parameters. Defaults to use chart's values.
      - 'key1=value1'
      - 'key2=value2'
      values_param: # Optional: List of files/URLs to values files. Defaults to use chart's values.
      - <local file1>
      - <url1>
      - <local file2>
      - <url2>
      flags: '' # Optiona: String with additional flags to pass to the helm command
    action: <apply|create> # Optional: Defaults to 'apply'
    namespace: <target_openshift_namespace>
```

You have the choice of sourcing a `file` or a `template`. The `file` definition expects that the sourced file has all definitions set and will NOT accept any parameters (i.e.: static content). The `template` definition can be paired with a `params` file and/or params supplied through a dictionary variable `params_from_vars` which will be passed into the template. Note that if a template supply all default values, it can be processed without `params` or `params_from_vars` set.

**_TIP:_** Both `file` and `template` choices give you the option of defining target namespaces in the template manually, or adding the `namespace` variable alongside the template and params (where applicable).

The `tags` definition is a list of tags that will be processed if the `include_tags` variable/fact is supplied. See [Filtering content based on tags](README.md#filtering-content-based-on-tags) below for more details.

The pre/post definitions are a set of pre and post roles to execute before/after a particular portion of the inventory is applied. This can be before/afterthe object levels - i.e.: before and after all of the content, or before/after certain files/templates at a content level.

### Template processing
Openshift-applier supports multiple template languages, that can be used to process your Openshift/Kubernetes Object Resources prior to being applied to the cluster.
Both templating engines support both local and remote template location (http(s)).
The currently supported template languages are:
- [Openshift templates](https://docs.openshift.com/container-platform/latest/openshift_images/using-templates.html)
- [Jinja templates](https://jinja.palletsprojects.com/)
- [Helm Charts](https://helm.sh/docs/topics/charts/)
- [Kustomize 2.x](https://kustomize.io/)

Openshift templates will require the use of `template` when sourcing your object resource(s). Use `params` to pass variables to the template.
```yaml
openshift_cluster_content:
- object:
  content:
  - name: Applying Openshift template
    template: "{{ inventory_dir }}/../.openshift/templates/template.yml"
    params:
      PARAM1: foo
      PARAM2: bar
```

Jinja templates can use either `file` or `template` when sourcing your object resources(s). Use `template` if your generated object resource is an Openshift template, otherwise use `file`.
```yaml
openshift_cluster_content:
- object:
  content:
  - name: Applying Openshift template
    file: "https://example.com/openshift/files/file.j2"
    jinja_vars:
      key1: value1
      key2: value2
```
Ansible variables are available and can be used in the Jinja template. Any variable required by the jinja template(s) can be passed through the `jinja_vars` dictionary (this is useful if you're using the same jinja template multiple times in your inventory). The `jinja_vars` are using `set_fact` and thus has precedence over host_vars and group_vars, see [Ansible variable precedence](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variable-precedence-where-should-i-put-a-variable) for more info.
Additional examples are available in the [test directory](https://github.com/redhat-cop/openshift-applier/tree/master/tests/files/jinja-templates)

**NOTE: In order to use the jinja processing engine the file suffix must be '.j2'**

Helm charts use a `helm` dictionary to source the chart into a `helm template` command. It will use the default `values.yaml` file, but various overrides exists to feed custom values to the charts. The complete list of supported parameters is above, but the values file can be substituted by supplying one or more files (or URLS) with the `values_param`, and the `set_param` can be used to inject individual values during the processing of the charts.
```yaml
openshift_cluster_content:
- object:
  content:
  - name: Apply a Helm Chart
    helm:
      name: Test Chart
      chart: "{{ inventory_dir }}/../../helm-charts/test-chart/"
      values_param:
        - "{{ inventory_dir }}/../../helm-charts/test-chart/values-test.yaml"
```    
Additional examples are available in the [helm charts test directory](https://github.com/redhat-cop/openshift-applier/tree/master/tests/files/helm-charts)

Kustomize templates can be processed using the `kustomize` field.

```
- object: configmap generator
  content:
  - name: configmap
    kustomize: "{{ inventory_dir }}/../../files/kustomize/"
    namespace: "{{ namespace_metadata.NAMESPACE }}-template-dev"
```

**NOTE: Kustomize templates will be invoked using `oc/kubectl apply -k /path/to/kustomize/`, and a such, only Kustomize 2.x will be supported.**

### Using oc vs kubectl

OpenShift-Applier is compatible with both `kubectl` and `oc` as a client binary. The client can be selected by setting `client: <oc|kubectl>` in any of your vars files, or as an inline ansible argument. **Default: `client: oc`**

YAML Example:
```yaml
client: kubectl

openshift_cluster_content:
...
```

INLINE Argument Example:
```bash
ansible-playbook -i .applier/ playbooks/openshift-cluster-seed.yml -e client=oc
```

**NOTE: If you have `client: kubectl`, but have OpenShift Templates in your inventory (defined by .object[*].content.template), you still need to have `oc` in your PATH.**

### Sourcing a directory with files

You can source a directory composed of static files (without parameters) using `files` instead of defining each file individually.

That would look like this:
```yaml
- object: policy
  content:
  - name: directory of files
    file: <path-to>/directory/
```
In this example above, all of the files in the `<path-to>/directory/` directory would get sourced and applied to the cluster (native OpenShift processing).

### Ordering of Objects in the inventory

The inventory content is defined as an ordered list, and hence processed in the order it is written. This is important to understand from the perspective of dependencies between your inventory content. For example; it's important to have namespaces or projectrequests defined early to ensure these exists before any of the builds or deployments defined later on in the inventory attempts to use a namespace.

One of the ways to define an OpenShift project using a file or template is to use define a `namespace` object. It would look like this:
```yaml
- object: namespace
  content:
  - name: <namespace_name>
    file: <file_source>
```

### Privileged Objects

Note that the `openshift-applier` runs at the permission level a user has, and hence defining objects requiring elevated privileges also requires the user running the `openshift-applier` to have the same level (or higher) of access to the OpenShift cluster.

### Object Entries in the Inventory

Objects and entries can be named as you please. In these objects definitions, you source templates that will add any in-project OpenShift objects including buildconfigs, deploymentconfigs, services, routes, etc. (*note:* these are standard OpenShift templates and no limitations is imposed from the `openshift-applier` for this content).

You can source as many templates and static files as you like.

These objects look like this:
```yaml
- object: <relevant_name>
  content:
  - name: <name_of_first_template>
    template: <template_source>
    params: <params_file_source>
    namespace: <target_namespace>
  - name: <name_of_second_template>
    template: <template_source>
    params_from_vars: <params_dictionary_variable>
    namespace: <target_namespace>
  - name: <name_of_file>
    file: <yaml/json_source>
    namespace: <target_namespace>
- object: <relevant_name>
  content:
  - name: <name_of_another_template>
    template: <template_source>
    params: <params_file_source>
    namespace: <target_namespace>
```

**_NOTE:_** The objects are sourced and applied in the order found in the list. For objects with inter-dependencies, it is important to consider the order these are defined.

**_NOTE:_** If the target namespace is not defined in each of the objects within the template, be sure to add the `namespace` variable.


### Override default actions with `action`

The file and template entries have default handling of `apply` - i.e.: how the `oc` command applies the object(s). This can be overridden with with the inventory variable `action`. Normally this should not be necessary, but in some cases it may be for various reasons such as permission levels. One example is if a `ProjectRequest` is defined as a **template**. In that case, if a non-privileged user tries to apply the objects it will error out as the user's permissions do not allow for `oc apply` at the cluster scope. In that case, it will be required to override the action with `action: create`. For example:

```yaml
openshift_cluster_content:
- object: projectrequest
  content:
  - name: "my-space1"
    file: "my-space.yml"
  - name: "my-space2"
    template: "my-space-template.yml"
    params: "my-space-paramsfile"
    action: create       # Note the 'action' set to override the default 'apply' action
  - name: "my-space3"
    template: "my-space-template.yml"
    params_from_vars: "{{ my_space_params_dict }}"
    action: create       # Note the 'action' set to override the default 'apply' action
```

**_NOTE:_** In the above example, the `my_space_params_dict` variable may look similar to the following:
```yaml
my_space_params_dict:
  NAMESPACE: my-project
  NAMESPACE_DISPLAY_NAME: MyProject
  NAMESPACE_DESCRIPTION: This is My Project
```

Valid `action` values are `apply`, `create`, `patch` and `delete`.

#### Using patch

Patching resources using applier can be done as follows:

```yaml
- object: single patch
  content:
  - name: patch a resource
    file: "route1.yml" # File containing the resource you would like to patch
    params: "patch.yml" # File containing the patch you would like to apply
    action: patch
```

An example of what a patch file might look like is:

```yaml
metadata:
  labels:
    labelkey: labelvalue
```

### Passing extra arguments to the client

OpenShift Applier supports passing additional argument flags to the client (`oc` or `kubectl`). This can be done by setting `.openshift_cluster_content.object.content[*].flag` to any string value.

For example, to explicitly set the patch strategy (`--type`) on a patch action:

```yaml
- object: json merge patch
  content:
  - name: perform json merge patch with flag
    file: "https://k8s.io/examples/application/deployment-patch.yaml"
    params: "{{ inventory_dir }}/../../files/patches/patch-demo-merge.yaml"
    action: patch
    flags: --type merge
```


### Filtering content based on tags

The `openshift-applier` supports the use of tags in the inventory (see example above) to allow for filtering which content should be processed and not. The `include_tags` and `exclude_tags` variables/facts take a comma separated list of tags that will be processed. The `include_tags` will apply content **only** with the matching tags, while `exclude_tags` will apply **anything but** the content with the matching tags.

**_NOTE:_** Entries in the inventory without tags will not be processed when a valid list of tags is supplied with `include_tags`.

**_NOTE:_** If the same tag exists in both `include_tags` and `exclude_tags` the run will error out. Likewise, if tags from the two options annuls each other, the execution will also error out.

```params
include_tags=tag1,tag2
exclude_tags=tag3,tag4

```

### Suppressing log output

Output can be suppressed either at the `object` or `content` level when there is a desire to suppress secret values from being displayed.

### Pre/Post steps

The `openshift-applier` supports the use of pre and post steps to allow for tasks to be executed before / after content is loaded up in OpenShift. This can be useful for things like:
 - waiting on a deployment to become ready before proceeding to the next
 - seeding the application with content after deployment
 - applying additional tweaks to the OpenShift objects post deployment (e.g.: labels, env variables, etc.)

The pre/post steps can be added at both the `object` level as well as the `content level`. See example at the top for more details.

In essence, the pre/post steps are ansible roles that gets executed in the order they are found in the inventory. These roles are sourced from the `galaxy_sources` list, or `galaxy_requirements` file, part of the inventory. See the official [Ansible Galaxy docs for more details on the requirements yaml file](http://docs.ansible.com/ansible/latest/galaxy.html#installing-multiple-roles-from-a-file).

**_NOTE:_** it is important that the repos used for pre/post roles have the `meta/main.yml` file setup correctly. See the [Ansible Galaxy docs](http://docs.ansible.com/ansible/latest/galaxy.html) for more details.

For roles that requires input parameters, the implementation also supports supplying variables, as part of the inventory, to the pre/post steps. See example at the top for more details.

### Deprovisioning

The `openshift-applier` role also supports global deprovisioning of resources. This can be done either using `provision: false`. Setting `-e provision=false` on a run essentially acts like a big 'undo' button, re-running all files and templates through `oc delete -f <resources>`. This can be useful when you want to do a full cleanup to ensure the integrity of you IaC repo, or for simple cleanup while testing changes.

### Dependencies

- openshift-login: Ansible role used to login a user to the OpenShift cluster.


## Example Playbook

TBD

## License

BSD

## Author Information

Red Hat Community of Practice & staff of the Red Hat Open Innovation Labs.
