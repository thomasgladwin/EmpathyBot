import emodet

while True:
    text_all = input("Tell me about it (Q to stop): ")
    if text_all.upper() == 'Q':
        break
    emodet.emodet(text_all)
