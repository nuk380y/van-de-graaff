from textnode import TextNode, TextType


def main():
    test = TextNode("test text", TextType.LinkText, "https://start.duckduckgo.com")

    print(test)


main()
