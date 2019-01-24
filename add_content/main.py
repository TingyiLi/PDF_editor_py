from pdf_utils import MyPDFHandler,PDFHandleMode as mode

def main():
    pdf_handler = MyPDFHandler(u'Digital-Speech-Transmission-Enhancement-Coding-and-Error-Concealment.pdf',mode = mode.NEWLY)
    pdf_handler.add_bookmarks_by_read_txt('./bookmarks-eclipse_plutin.txt',page_offset = 11)
    pdf_handler.save2file(u'Speech_Audio.pdf')

if __name__ == '__main__':
    main()
