from textnode import TextNode, TextType


def main():
    dummyVal = TextNode(
        "This is some anchor text", TextType.LINK_TEXT, "https://www.boot.dev"
    )

    print(dummyVal)


main()
