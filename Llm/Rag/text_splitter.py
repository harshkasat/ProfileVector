from langchain.text_splitter import RecursiveCharacterTextSplitter


def recursive_text_splitter(text):

    try:

        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 100,
        chunk_overlap  = 20,
        length_function = len,
        )
        split_texts = text_splitter.split_text(text)

        return split_texts
    
    except Exception as e:
        print(f"An error occurred when Recursive Character Text Splitter: {e}")
        return None


# if __name__ == '__main__':
#     username = "harshkasat"
#     text_splitter(username)
