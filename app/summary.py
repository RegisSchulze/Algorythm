#import packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import re
import os 
import wget
from transformers import BartTokenizer, BartForConditionalGeneration
import torch

#create class summarization to be used by Flask
class summarization():

# 2 methods are created
# 1) get_book, with parameter name = name of the book which will download the correct .txt file from https://www.gutenberg.org/
# of that book and return a value chapter_folder(containing numbers; ex. 203-0.txt) which is how they named the book on https://www.gutenberg.org/
    def get_book(name):

        # initialise selenium webdriver and open chrometab
        PATH = "/usr/bin/chromedriver"
        driver = webdriver.Chrome(PATH)
        driver.maximize_window()

        # go to https://www.gutenberg.org/
        driver.get("https://www.gutenberg.org/")
        driver.implicitly_wait(20)
        chapter_folder=''

        # search for book with inputed name
        driver.find_element(By.ID,'menu-book-search').send_keys(name)
        driver.implicitly_wait(20)
        
        # press go button
        element = driver.find_element_by_xpath("/html/body/div[1]/nav/div[2]/div/form/input[2]")
        element.click()
        driver.implicitly_wait(20)
        
        # check how many versions of this particular book there are
        inputboxes=driver.find_elements(By.CLASS_NAME,'booklink')
        
        # find all the links on this page; meaning all href tags 
        elems = driver.find_elements_by_xpath("//a[@href]")
        elems_href=[]

        # from these links only look for ones containing numbers as these are links to the different book versions
        for elem in elems:
            if re.search(r'/\d+', elem.get_attribute("href")):
                elems_href.append(elem.get_attribute("href"))
        # close chrometab
        driver.quit()
        
        # we have either books that have only one version(one link with numbers) or with several versions (several links with numbers)
        # if only one version
        if len(elems_href)==1:
            link=elems_href[0]
            PATH = "/usr/bin/chromedriver"
            driver = webdriver.Chrome(PATH)
            
            # go to link of  book
            driver.get(link)

            # find all links for this book (different formats of book; kindle, html, txt, ...)
            elems = driver.find_elements_by_xpath("//a[@href]")
            elems_href=[]
            for elem in elems:
                elems_href.append(elem.get_attribute("href"))
            
            # we want to download the .txt file of the book
            # select links containing .txt
            matching = [s for s in elems_href if ".txt" in s]

            # quit chrometab
            driver.quit()
            
            #download .txt file of the particular book
            s=r'wget '+matching[0]

            # use os package to automate command line excecutions from within a .py file
            os.system(s)
            
            # use chapterize package to chapterize the book
            # this returns directory .../Algorythm/{chapter_folder}/
            s=r'chapterize '+matching[0].split('/')[-1]

            # get the chapter folder name
            chapter_folder=matching[0].split('/')[-1].split('.')[0]

            #chapterize the book from command line
            os.system(s)
            
        # if more than one version of the book   
        else:
        
        # get the first two book versions, reason for this is that some books have .txt files that are not containing the full book
        # books with several versions can also be written in different languages, however the first versions are always english
        # so selection of first two versions is done with this in mind
            link=elems_href[0]
            link2=elems_href[1]
        
            # open new chrometab
            PATH = "/usr/bin/chromedriver"
            driver = webdriver.Chrome(PATH)
            # go to first book version
            driver.get(link)

            # select all links on this page
            elems = driver.find_elements_by_xpath("//a[@href]")
            elems_href=[]
            for elem in elems:
                elems_href.append(elem.get_attribute("href"))

            # select .txt version of the book
            matching = [s for s in elems_href if ".txt" in s]

            # quit chrometab
            driver.quit()

            # open new chrometab
            PATH = "/usr/bin/chromedriver"
            driver = webdriver.Chrome(PATH)

            # go to second book version
            driver.get(link2)
            
            # select all links on this page
            elems = driver.find_elements_by_xpath("//a[@href]")
            elems_href=[]
            for elem in elems:
                elems_href.append(elem.get_attribute("href"))

            # select .txt version of the book
            matching2 = [s for s in elems_href if ".txt" in s]

            # quit chrometab
            driver.quit()
        
            # extract body of txt file of first book version to get idea of lenght text, to check if its the full version
            PATH = "/usr/bin/chromedriver"
            driver = webdriver.Chrome(PATH)
            driver.get(matching[0])

            l=driver.find_element_by_css_selector("body")
            text=l.text
            driver.quit()
            
            # extract body of txt file of second book version to get idea of lenght text, to check if its the full version
            PATH = "/usr/bin/chromedriver"
            driver = webdriver.Chrome(PATH)
            driver.get(matching2[0])

            l=driver.find_element_by_css_selector("body")
            text2=l.text
            driver.quit()

            # decide which book version to chose based on book length version 1 and 2
            # if first book version long enough
            if len(text)/len(text2)>0.7:

                #download .txt file of the first book version
                s=r'wget '+matching[0]
                os.system(s)
            
                # use chapterize package to chapterize first book version
                # this returns directory .../Algorythm/{chapter_folder}/
                s=r'chapterize '+matching[0].split('/')[-1]
                chapter_folder=matching[0].split('/')[-1].split('.')[0]
                os.system(s)
            # if first book version not complete book, chose second version
            else:
                #download .txt file of the second book version
                s=r'wget '+matching2[0]
                os.system(s)

                # this returns directory .../Algorythm/{chapter_folder}/
                s=r'chapterize '+matching2[0].split('/')[-1]
                chapter_folder=matching2[0].split('/')[-1].split('.')[0]
                os.system(s)
        
        # return name of chapter folder of the chapterized book
        return chapter_folder

    # 2) method create_summary to create summary of the book with pytorch and Bart
    def create_summary(chapter_folder):
        # initialise list that will be appended with each chapter resulting in the full book summary
        full_summary=[]
        dir_chapters=r'/home/regis/Desktop/Algorythm/Project/Algorythm/'+chapter_folder+'-chapters/' 
        
        # create list that contains all the chapter file paths
        files=[]
        for filename in os.listdir(dir_chapters):
            if filename.endswith(".txt"): 
                files.append(filename)
                continue
            else:
                continue

        # sort these file paths as we want our summary to be in correct order; chapter 1 followed by chapter 2, ...
        files_sorted=sorted(files)
        chapters=[]
        for i in files_sorted:
            s=r''+dir_chapters+''+i
            chapters.append(s)

        # summarize on each individual chapter
        for i in chapters:
            with open(i) as f:

                # read content of .txt file of particular chapter 
                contents = f.read()
                model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
                tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
                
                # tokenize without truncation
                inputs_no_trunc = tokenizer(contents, max_length=None, return_tensors='pt', truncation=False)

                # get batches of tokens corresponding to the exact model_max_length
                chunk_start = 0
                chunk_end = tokenizer.model_max_length #  == 1024 for Bart
                inputs_batch_lst = []
                while chunk_start <= len(inputs_no_trunc['input_ids'][0]):
                    inputs_batch = inputs_no_trunc['input_ids'][0][chunk_start:chunk_end]  # get batch of n tokens
                    inputs_batch = torch.unsqueeze(inputs_batch, 0)
                    inputs_batch_lst.append(inputs_batch)
                    chunk_start += tokenizer.model_max_length #  == 1024 for Bart
                    chunk_end += tokenizer.model_max_length  # == 1024 for Bart

                # generate a summary on each batch
                summary_ids_lst = [model.generate(inputs, num_beams=4, max_length=100, early_stopping=True) for inputs in inputs_batch_lst]

                # decode the output and join into one string with one paragraph per summary batch
                summary_batch_lst = []
                for summary_id in summary_ids_lst:
                    summary_batch = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_id]
                    summary_batch_lst.append(summary_batch[0])
                summary_all = '\n'.join(summary_batch_lst)
                full_summary.append(summary_all)
        # return list containing full summary of the book
        return full_summary