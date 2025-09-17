from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
        else:
            fragments = node.text.split(delimiter)

            if len(fragments) % 2 == 0:
                raise SyntaxError("unmatched delimiter")

            for frag in fragments:
                if fragments.index(frag) % 2 != 0:
                    frag = TextNode(frag, text_type)
                else:
                    # elif fragments.index(frag) % 2 == 0:
                    frag = TextNode(frag, node.text_type)

            new_nodes.extend(fragments)

    return new_nodes
