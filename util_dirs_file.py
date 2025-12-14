def is_dir(node, name):
    return name in node and isinstance(node[name], dict)
def is_file(node, name):
    return name in node and isinstance(node[name], str)