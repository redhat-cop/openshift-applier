import os
import urllib
try:
    from urlparse import urljoin
    from urllib import urlopen
except ImportError:
    from urllib.parse import urljoin
    from urllib.request import urlopen


# Return content invoked with improper tag usage
def get_invalid_tag_usage(applier_list, include_tags, exclude_tags):

    if len(include_tags.strip()) == 0 or len(exclude_tags.strip()) == 0:
        return []

    # Convert comma seperated list to an actual list and strip off whitespaces of each element
    include_list = include_tags.split(",")
    include_list = [i.strip() for i in include_list]

    exclude_list = exclude_tags.split(",")
    exclude_list = [i.strip() for i in exclude_list]

    repeated_tags = []
    # Loop through the main list to check if any tags were invoked incorrectly
    # - append to repeated_tags and return
    for a in applier_list[:]:
        if 'content' in a:
            for c in a['content'][:]:
                if 'tags' not in c:
                    continue

                include_matches = list(set(include_list) & set(c['tags']))

                exclude_matches = list(set(exclude_list) & set(c['tags']))

                if include_matches and exclude_matches:
                    repeated_tags.append({
                        'object': a.get("object", "[unknown]"),
                        'name': c.get("name", "[unknown]"),
                        'invoked_tags': include_matches + exclude_matches,
                    })

    return repeated_tags


# Helper function to simplify the 'filter_applier_item' below
def filter_content(content_dict, outer_list, include_list, exclude_list):
    # Handle if tags don't exist in the 'content' section
    if 'tags' not in content_dict:
        if include_list:
            outer_list.remove(content_dict)
        return

    # Handle if include_tags exists in the 'content' section
    if include_list:
        intersect_list = [
            val for val in content_dict['tags'] if val in include_list]
        if len(intersect_list) == 0:
            outer_list.remove(content_dict)
            return

    # Handle if exclude_tags exists in the 'content' section
    if exclude_list:
        intersect_list = [
            val for val in content_dict['tags'] if val in exclude_list]
        if len(intersect_list) != 0:
            outer_list.remove(content_dict)
            return


# Main 'filter_applier_item' function
def filter_applier_item(applier_item, include_tags, exclude_tags):
    # If no tag lists supplied - just return item
    if len(include_tags.strip()) == 0 and len(exclude_tags.strip()) == 0:
        return applier_item

    exclude_list, include_list = [], []

    # Convert comma seperated list to an actual list and strip off whitespaces of each element
    if include_tags and len(include_tags.strip()) != 0:
        include_list = include_tags.split(",")
        include_list = [i.strip() for i in include_list]

    if exclude_tags and len(exclude_tags.strip()) != 0:
        exclude_list = exclude_tags.split(",")
        exclude_list = [i.strip() for i in exclude_list]

    # Handle the 'content' entries
    if 'content' in applier_item:
        for c in applier_item['content'][:]:
            filter_content(c, applier_item['content'], include_list, exclude_list)

    return applier_item


# Function used to determine a files location - i.e.: URL, local file/directory or "something else"
def check_file_location(path):
    # default return values
    return_vals = {
        "oc_option_f":  '',
        "oc_path": path,
        "oc_process_local": '',
        "local_path": False
    }

    # default return status to false
    url_status = False

    # First try to see if this is a local file or directory - if it is not, check for a valid URL
    path_status = os.path.exists(path)
    if (not path_status):
        try:
            url_status = urlopen(path)
        except (IOError, ValueError):
            # Must be a pre-loaded template, nothing to do
            return return_vals

    # If it is a valid URL or local file, set the proper flags
    if ((url_status and url_status.getcode() == 200) or path_status):
        return_vals['oc_option_f'] = ' -f'
        return_vals['oc_process_local'] = ' --local'

    # If this is a local file, set flag to indicate so
    if (path_status):
        if (os.path.isdir(path)):
            return_vals['oc_path'] += '/'
        return_vals['local_path'] = True

    return return_vals


class FilterModule(object):
    ''' Filters to handle openshift_cluster_content data '''

    def filters(self):
        return {
            'check_file_location': check_file_location,
            'filter_applier_item': filter_applier_item,
            'get_invalid_tag_usage': get_invalid_tag_usage
        }
