import requests
from bs4 import BeautifulSoup
import subprocess
import sys
import typing
import sys
from tqdm import tqdm, trange
import time
from time import sleep
import os
import cpuinfo
from argParse import ArgParser

class Color:
    def __init__(self) -> None:
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKCYAN = '\033[96m'
        self.OKGREEN = '\033[92m'
        self.YELLOW = '\033[33m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'
    def green(self, txt):
        return self.OKGREEN+txt+self.ENDC
    def purple(self, txt):
        return self.HEADER+txt+self.ENDC
    def red(self, txt):
        return self.FAIL+txt+self.ENDC
    def yellow(self, txt):
        return self.YELLOW+txt+self.ENDC
class console:
    bar = Color().yellow('-'*20)
color = Color()
special, file_name, prob_num = None, None, None
# https://patorjk.com/software/taag 
#? Font : types
# https://www.ditig.com/publications/256-colors-cheat-sheet
titleMsg = '\033[38;5;118m'+'''
 .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |   ______     | || |     ____     | || |     _____    | || |              | || |  ___  ____   | || |  _______     | |
| |  |_   _ \\    | || |   .'    `.   | || |    |_   _|   | || |              | || | |_  ||_  _|  | || | |_   __ \\    | |
| |    | |_) |   | || |  /  .--.  \\  | || |      | |     | || |              | || |   | |_/ /    | || |   | |__) |   | |
| |    |  __'.   | || |  | |    | |  | || |   _  | |     | || |              | || |   |  __'.    | || |   |  __ /    | |
| |   _| |__) |  | || |  \\  `--'  /  | || |  | |_' |     | || |      _       | || |  _| |  \\ \\_  | || |  _| |  \\ \\_  | |
| |  |_______/   | || |   `.____.'   | || |  `.___.'     | || |     (_)      | || | |____||____| | || | |____| |___| | |
| |              | || |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
'''+color.ENDC
successMsg = color.OKGREEN+'''success'''+color.ENDC
failMsg = '\033[48;5;160m'+'''
 .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |  _________   | || |      __      | || |     _____    | || |   _____      | || |              | || |              | |
| | |_   ___  |  | || |     /  \\     | || |    |_   _|   | || |  |_   _|     | || |              | || |              | |
| |   | |_  \\_|  | || |    / /\\ \\    | || |      | |     | || |    | |       | || |              | || |              | |
| |   |  _|      | || |   / ____ \\   | || |      | |     | || |    | |   _   | || |              | || |              | |
| |  _| |_       | || | _/ /    \\ \\_ | || |     _| |_    | || |   _| |__/ |  | || |      _       | || |      _       | |
| | |_____|      | || ||____|  |____|| || |    |_____|   | || |  |________|  | || |     (_)      | || |     (_)      | |
| |              | || |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
'''+color.ENDC

config = '''
채점시간 : {}
실행환경 : {}
'''

#? 로딩창

# https:/dreamhack.io/\@0.0.0.0:80/flag#
#! 업데이트할거
#? 0. 실행시간, UI개선
#? 1. 틀리면 data, output 출력
#? 2. 스페셜 저지
#? 100. vscode확장

cpu = cpuinfo.get_cpu_info()

isDir = lambda path: os.path.isdir(path)
isFile = lambda path: os.path.isfile(path)
isExist = lambda path: os.path.exists(path)


headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

class onlineJudge:
    def __init__(self, prob_num, file_name) -> None:
        # boj short url
        self.url = f'https://boj.kr/{prob_num}'
        self.prob_num = prob_num
        fp = os.path.join(os.getcwd(), file_name)
        
        if (os.path.exists(fp)):
            self.fp = fp
            self.file_name = file_name
        else:
            raise FileExistsError(f'Filename {fp} is not exist')

    def getTests(self):
        response = requests.get(self.url, headers=headers)

        if response.status_code != 200: print('Error : '+str(response.status_code))

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        self.title = soup.select_one('#problem_title').text
        self.description = soup.select_one('#problem_description').text
        self.input_section = soup.select_one('#problem_input').text
        self.output_section = soup.select_one('#problem_output').text
        
        samples = soup.select('#problem-body .col-md-12 .row .col-md-6')

        sample_inputs = []
        sample_outputs = []
        
        for idx in range(0,len(samples)//2):
            input, output = samples[idx*2], samples[idx*2+1]

            sample_input = input.select_one(f'#sample-input-{idx+1}')
            sample_output = output.select_one(f'#sample-output-{idx+1}')

            # case handling
            if sample_input!=None and sample_input.text!='': 
                sample_inputs.append(sample_input.text.strip())
            if sample_output!=None and sample_output.text!='': 
                sample_outputs.append(sample_output.text.strip())

            # padding 처리
            # case - input이 없고, output만 있는 경우
            # input : ""
            # output : "1234"
            if len(sample_inputs)>len(sample_outputs) : 
                sample_outputs.append('')
            elif len(sample_outputs)>len(sample_inputs) :
                sample_inputs.append('')

            if sample_input==None and sample_input.text=='' and sample_output==None and sample_output.text=='': break
        self.sample_inputs, self.sample_outputs = sample_inputs, sample_outputs
        return sample_inputs, sample_outputs
    def sanitizeData(self, txt):
        txt = txt.replace('\r','')
        return txt
    def execFile(self, input:str):
        assert type(input) == str

        fp = os.path.join(os.getcwd(), self.file_name)

        if not isExist(fp): raise FileExistsError(f'Filename {fp} is not exist')
        
        _, ext = os.path.splitext(fp)
        try:
            if(ext == '.py'):
                cmd = f'''python {fp}'''
                
                pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
                data = pipe.communicate(input=input.encode())[0].decode()
                return data.strip()
            elif(ext == '.js'):
                cmd = f'''node {fp}'''
                
                pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
                data = pipe.communicate(input=input.encode())[0].decode()
                return data.strip()
            elif(ext == '.c'):
                exe = ''.join(fp.split('.')[:-1])
                cmd = f'''gcc {fp} -o {exe}'''
                pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
                data = pipe.communicate(input=input.encode())[0].decode()
                cmd = f'''{exe}'''
                pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
                data = pipe.communicate(input=input.encode())[0].decode()
                return data.strip()
            else:
                print(f'File Format {ext} is not supported')
                exit()
        except:
            raise Exception(color.red("파일 실행 중 에러 발생 (입력형식확인)"))
    def test(self):
        isSuccess = True
        ncols = 10*len(samples_i)
        with tqdm(total=len(samples_i),ascii=' =',ncols=ncols) as pbar:
            for idx, (sample_i, sample_o) in enumerate(zip(samples_i, samples_o)):
                sleep(0.2)
                pbar.update(10)
                
                out = self.execFile(sample_i)
                out = self.sanitizeData(out)
                sample_o = self.sanitizeData(sample_o)

                if special: #? 스페셜 저지 구현 | 미완성
                    if int(out)-int(sample_o) < .1 ** special:
                        continue
                    else:
                        isSuccess = False
                        break
                elif out != self.sanitizeData(sample_o):
                    isSuccess = False
                    break
        if isSuccess: 
            print(color.green(successMsg))
        else:
            print('\n',console.bar)
            print(color.red(failMsg))
            print("<input>")
            print(sample_i)
            print("<output>")
            print(sample_o)
            print("<your answer>")
            print(out)

if __name__ == '__main__':
    print(titleMsg)


    args = ArgParser()
    args.addInt('prob')
    args.addStr('f')
    args.addInt('s')
    parsed = args.get()

    if 's' in parsed.keys():
        special = parsed['s']
    if 'prob' in parsed.keys():
        prob_num = parsed['prob']
    else:
        prob_num = input("PROBLEM_NUMBER : ")

    if 'f' in parsed.keys():
        if parsed['f'].split('.')[-1] in ['py', 'c', 'js']:
            file_name = parsed['f']
        else:
            raise KeyError('file extension is not supported')
    else:
        print('Default filename is {}.py'.format(prob_num))
        file_name = input('FILE_NAME : ')
        if file_name == None or file_name.strip() == '':
            file_name = f'{prob_num}.py'
            
    fp = os.path.join(os.getcwd(), file_name)
    if not os.path.exists(fp): raise FileNotFoundError(f'{fp} is not found')

    show_samples = True
    judge = onlineJudge(prob_num, file_name)
    samples_i, samples_o = judge.getTests()
    
    print(config.format(time.strftime("%Y-%m-%d %H:%M:%S"), cpu['brand_raw']))

    print(console.bar)

    print(f'''{color.purple(f'Title : {judge.title}')} 
Description : {judge.description.replace('\n\n','\n').strip()} 
{console.bar}
Input : {judge.input_section.strip().replace('\n\n','\n')}      
Output : {judge.output_section.strip().replace('\n\n','\n')}''')
    
    judge.test()