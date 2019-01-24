from PyPDF2 import PdfFileReader as reader,PdfFileWriter as writer
import os

class PDFHandleMode(object):
    '''
    processing mode
    '''
    # Keep original imformation
    COPY = 'copy'
    NEWLY = 'newly'

class MyPDFHandler(object):
    def __init__(self,pdf_file_path,mode = PDFHandleMode.COPY):
        '''
        :param pdf_file_path
        :param mode
        '''
        self.__pdf = reader(pdf_file_path)

        # pdf file name(without path name)
        self.file_name = os.path.basename(pdf_file_path)
        #
        self.metadata = self.__pdf.getXmpMetadata()
        #
        self.doc_info = self.__pdf.getDocumentInfo()
        #
        self.pages_num = self.__pdf.getNumPages()

        self.__writeable_pdf = writer()
        if mode == PDFHandleMode.COPY:
            self.__writeable_pdf.cloneDocumentFromReader(self.__pdf)
        elif mode == PDFHandleMode.NEWLY:
            for idx in range(self.pages_num):
                page = self.__pdf.getPage(idx)
                self.__writeable_pdf.insertPage(page, idx)

    def save2file(self,new_file_name):
        '''
        :param new_file_name: new name
        :return: None
        '''
        # 保存修改后的PDF文件内容到文件中
        with open(new_file_name, 'wb') as fout:
            self.__writeable_pdf.write(fout)
        print('save2file success! new file is: {0}'.format(new_file_name))

    def add_one_bookmark(self,title,page,parent = None, color = None,fit = '/Fit'):
        self.__writeable_pdf.addBookmark(title,page - 1,parent = parent,color = color,fit = fit)
        print('add_one_bookmark success! bookmark title is: {0}'.format(title))

    def add_bookmarks(self,bookmarks):
        for title,page in bookmarks:
            self.add_one_bookmark(title,page)
        print('add_bookmarks success! add {0} pieces of bookmarks to PDF file'.format(len(bookmarks)))

    def read_bookmarks_from_txt(self,txt_file_path,page_offset = 0):
        bookmarks = []
        with open(txt_file_path,'r') as fin:
            for line in fin:
                line = line.rstrip()
                if not line:
                    continue
                # @ seperate name and page number
                print('read line is: {0}'.format(line))
                try:
                    title = line.split('@')[0].rstrip()
                    page = line.split('@')[1].strip()
                except IndexError as msg:
                    print(msg)
                    continue
                if title and page:
                    try:
                        page = int(page) + page_offset
                        bookmarks.append((title, page))
                    except ValueError as msg:
                        print(msg)

        return bookmarks

    def add_bookmarks_by_read_txt(self,txt_file_path,page_offset = 0):
        bookmarks = self.read_bookmarks_from_txt(txt_file_path,page_offset)
        self.add_bookmarks(bookmarks)
        print('add_bookmarks_by_read_txt success!')
