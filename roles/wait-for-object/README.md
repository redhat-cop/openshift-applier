# Wait-for-resource

## What does this role do?

This role allows you to specify a serious of variables and waits until it is able to see these resources available within a cluster.

## Variables
- k8s_object:
- k8s_object_name:
- k8s_object_namespace:
- k8s_object_wait_seconds:


## Parameters

| Name      | Description   | Required | Default |
| ----------- | ----------- | -------- | ------- |
| k8s_object | The type of k8s object that you're waiting on (pod, configmap, etc.) | Y | N/A |
| k8s_object_name | The name of the k8s object that you're waiting on. Will look for all objects of a type if no name is specified | N | N/A |
| k8s_object_namespace | The namespace of the k8s object that you're waiting on. Will look for all objects in all namespaces if no namespace is specified | N | N/A |
| k8s_object_wait_seconds | The number of "warm-up" seconds to give an object before checking for its existance. | N | 0 |

## Example

```yaml
- hosts: my-test-hosts 
  tasks:
  - name: Check for a configmap
    include_role:
      name: roles/wait-for-object
    vars:
      k8s_object: configmap
      k8s_object_name: ldap-config
      k8s_object_namespace: cluster-ops
```
