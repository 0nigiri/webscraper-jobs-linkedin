from datetime import datetime
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd

now = datetime.now()
urlList = [
    "https://www.linkedin.com/jobs/search?keywords=Publicidade&location=Brasil&locationId=&geoId=106057199&f_TPR=&f_JT=F%2CI&f_WT=2&f_E=1%2C4%2C5%2C6&position=1&pageNum=0",
    "https://www.linkedin.com/jobs/search?keywords=Publicidade&location=Brasil&locationId=&geoId=106057199&f_TPR=&f_JT=F%2CI&f_E=2&f_WT=2&position=1&pageNum=0",
    "https://www.linkedin.com/jobs/search?keywords=Publicidade&location=Brasil&locationId=&geoId=106057199&f_TPR=&f_JT=F%2CI&f_WT=3&f_E=3%2C4%2C5&position=1&pageNum=0",
    "https://www.linkedin.com/jobs/search?keywords=Publicidade&location=Brasil&locationId=&geoId=106057199&f_TPR=&f_JT=F%2CI&f_E=1%2C2&f_WT=3&position=1&pageNum=0",
    "https://www.linkedin.com/jobs/search?keywords=Publicidade&location=Brasil&locationId=&geoId=106057199&f_TPR=&f_JT=F%2CI&f_WT=1&f_E=1%2C3%2C5&position=1&pageNum=0",
    "https://www.linkedin.com/jobs/search?keywords=Publicidade&location=Brasil&locationId=&geoId=106057199&f_TPR=&f_JT=F%2CI&f_E=4&f_WT=1&position=1&pageNum=0",
    "https://www.linkedin.com/jobs/search?keywords=Publicidade&location=Brasil&locationId=&geoId=106057199&f_TPR=&f_JT=F%2CI&f_E=2&f_WT=1&position=1&pageNum=0"
]


# urlteste = 'https://www.linkedin.com/jobs/search?keywords=Marinheiro&location=Brasil&geoId=106057199&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'


def startWebService(url):
    driver_service = Service(executable_path=ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'pt'})
    driver = webdriver.Chrome(service=driver_service, options=options)
    driver.maximize_window()
    driver.get(url)
    return driver


try:
    data = pd.read_csv('desafio.csv')
    idJob = data['id'].tolist()
    urlPage = data['URL da vaga no linkedin'].tolist()
    nomeVaga = data['Nome da vaga'].tolist()
    nomeEmpresa = data['Nome da empresa contratante'].tolist()
    urlEmpresa = data['URL da empresa contratante'].tolist()
    modeloContrato = data['Modelo de contratação'].tolist()
    tipoContrato = data['Tipo de contratação'].tolist()
    experiencia = data['Nível de experiência'].tolist()
    numCandidatos = data['Número de candidaturas para vaga'].tolist()
    dataPostagem = data['Data da postagem da vaga'].tolist()
    dataScrap = data['Horário do scraping'].tolist()
    numeroFuncionario = data['Número de funcionários da empresa'].tolist()
    numeroSeguidores = data['Número de seguidores da empresa'].tolist()
    localSedeEmpresa = data['Local sede da empresa'].tolist()
    urlCandidatura = data['URL da candidatura'].tolist()
except Exception as e:
    print(e)
    idJob = []
    urlPage = []
    nomeVaga = []
    nomeEmpresa = []
    urlEmpresa = []
    modeloContrato = []
    tipoContrato = []
    experiencia = []
    numCandidatos = []
    dataPostagem = []
    dataScrap = []
    numeroFuncionario = []
    numeroSeguidores = []
    localSedeEmpresa = []
    urlCandidatura = []


def check_id_exists_set(lst, target):
    return target in set(lst)


def saveProgress():
    job_data = pd.DataFrame({
        'id': idJob,
        'URL da vaga no linkedin': urlPage,
        'Nome da vaga': nomeVaga,
        'Nome da empresa contratante': nomeEmpresa,
        'URL da empresa contratante': urlEmpresa,
        'Modelo de contratação': modeloContrato,
        'Tipo de contratação': tipoContrato,
        'Nível de experiência': experiencia,
        'Número de candidaturas para vaga': numCandidatos,
        'Data da postagem da vaga': dataPostagem,
        'Horário do scraping': dataScrap,
        'Número de funcionários da empresa': numeroFuncionario,
        'Número de seguidores da empresa': numeroSeguidores,
        'Local sede da empresa': localSedeEmpresa,
        'URL da candidatura': urlCandidatura
    })
    job_data.to_csv('desafio.csv', index=False)
    print("Progress saved")


def getAllList(num):
    i = 0
    while i <= int(num / 25) + 5:
        try:
            if driver.find_element(By.CSS_SELECTOR,
                                   "p.inline-notification__text.text-sm.leading-regular").is_displayed():
                break
        except:
            pass
        checkNumberJobs = len(driver.find_elements(By.TAG_NAME, "li"))
        if checkNumberJobs >= 1000 or checkNumberJobs == int(
                num):
            break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            if driver.find_element(By.XPATH,
                                   ".//button[@aria-label='Ver mais vagas']").is_displayed() and driver.find_element(
                By.XPATH, ".//button[@aria-label='Ver mais vagas']").is_enabled():
                driver.execute_script("window.scrollTo(1000, document.body.scrollHeight);")
                time.sleep(1.5)
                driver.find_element(By.XPATH, ".//button[@aria-label='Ver mais vagas']").click()
                i = i + 1
            else:
                driver.execute_script("window.scrollTo(1000, document.body.scrollHeight);")
            continue
        except:
            time.sleep(1)
            continue

    print('starting scrap')


def scrapProcess(driver):
    try:
        job_lists = driver.find_element(By.CLASS_NAME, "jobs-search__results-list")
        jobs = job_lists.find_elements(By.TAG_NAME, "li")
        item = 0
        errorCount = 0
        for job in jobs:
            if errorCount == 50:
                saveProgress()
                time.sleep(10)
                driver.quit()
                return False
                break

            while True:
                if errorCount == 50:
                    break
                try:
                    job_click_path = f'/html/body/div/div/main/section/ul/li[{item + 1}]'
                    job_click = job.find_element(By.XPATH, job_click_path).click()

                    idJob_path = f'//*[@id="main-content"]/section[2]/ul/li[{item + 1}]/div | //*[@id="main-content"]/section[2]/ul/li[{item + 1}]/a'
                    try:
                        idJobNew = job.find_element(By.XPATH, idJob_path).get_attribute('data-entity-urn')
                        extractId = re.findall(r"[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",
                                               idJobNew)
                        for number in extractId:
                            idJobNew = int(number.replace(".", "").replace(",", ""))

                        if check_id_exists_set(idJob, idJobNew):
                            item += 1
                            break
                    except:
                        print("Erro ", errorCount, ":  fail catch jobs id")
                        errorCount += 1
                        continue


                    if not driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div[2]').is_displayed():
                        time.sleep(1)
                        job_click_path = f'/html/body/div/div/main/section/ul/li[{item}]'
                        job_click = job.find_element(By.XPATH, job_click_path).click()
                        time.sleep(1)
                        job_click_path = f'/html/body/div/div/main/section/ul/li[{item + 1}]'
                        job_click = job.find_element(By.XPATH, job_click_path).click()
                        errorCount += 1
                        continue
                except:
                    print("Erro ", errorCount, ":  click jobs")
                    errorCount += 1
                    continue
                time.sleep(1)

                urlPage_path = "//a[contains(@class, 'topcard__link')]"
                try:
                    urlPageNew = job.find_element(By.XPATH, urlPage_path).get_attribute('href')
                    if str(idJobNew) not in urlPageNew:
                        time.sleep(1)
                        job_click_path = f'/html/body/div/div/main/section/ul/li[{item}]'
                        job_click = job.find_element(By.XPATH, job_click_path).click()
                        time.sleep(1)
                        job_click_path = f'/html/body/div/div/main/section/ul/li[{item + 1}]'
                        job_click = job.find_element(By.XPATH, job_click_path).click()
                        continue


                except:
                    print('Erro ', errorCount, ": fail catch urlPage")
                    errorCount += 1
                    continue

                modeloContrato_path = '//button[contains(@data-tracking-control-name,"public_jobs_f_WT")]'
                try:
                    modeloContratoNew = job.find_element(By.XPATH, modeloContrato_path).get_attribute('innerText')
                    modeloContratoNew = modeloContratoNew.strip()
                except:
                    print('Erro ', errorCount, ": fail catch modelo contrato")
                    errorCount += 1
                    continue

                nomeVaga_path = '//h2[contains(@class, "top-card-layout__title")]'
                try:
                    nomeVagaNew = job.find_element(By.XPATH, nomeVaga_path).get_attribute('innerText')
                    nomeVagaNew = nomeVagaNew.strip()
                except:
                    print('Erro ", errorCount,":  fail catch nome vaga')
                    errorCount += 1
                    continue

                try:
                    description_list = driver.find_elements(By.XPATH,
                                                            "//li[contains(@class, 'description__job-criteria-item')]")

                    if len(description_list) == 4:
                        tipoContrato_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[2]/span'
                        try:
                            tipoContratoNew = job.find_element(By.XPATH, tipoContrato_path).get_attribute('innerText')
                            tipoContratoNew = tipoContratoNew.strip()

                        except:
                            print("Erro ", errorCount, ":  fail catch tipo Contrato")
                            errorCount += 1
                            continue

                        experiencia_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[1]/span'
                        try:
                            experienciaNew = job.find_element(By.XPATH, experiencia_path).get_attribute('innerText')
                            experienciaNew = experienciaNew.strip()
                        except:
                            print("Erro ", errorCount, ":  fail catch experiencia")
                            errorCount += 1
                            continue
                    else:
                        experienciaNew = 'N/E'

                        tipoContrato_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[1]/span'
                        try:
                            tipoContratoNew = job.find_element(By.XPATH, tipoContrato_path).get_attribute('innerText')
                            tipoContratoNew = tipoContratoNew.strip()

                        except:
                            print("Erro ", errorCount, ":  fail catch tipo Contrato")
                            errorCount += 1
                            continue

                except:
                    print("Erro ", errorCount, ":  fail catch  descricoes")
                    errorCount += 1
                    continue

                numCandidatos_path = '//*[contains(@class,"num-applicants__caption")]'
                try:
                    numCandidatosNew = job.find_element(By.XPATH, numCandidatos_path).get_attribute('innerText')
                    numCandidatosNew = numCandidatosNew.strip()
                except:
                    print("Erro ", errorCount, ":  fail catch numero candidatos")
                    errorCount += 1
                    continue

                dataPostagem_path = '//span[contains(@class,"posted-time-ago__text")]'
                try:
                    dataPostagemNew = job.find_element(By.XPATH, dataPostagem_path).get_attribute('innerText')
                    dataPostagemNew = dataPostagemNew.strip()
                except:
                    print("Erro ", errorCount, ":  fail catch data postagem")
                    errorCount += 1
                    continue

                nomeEmpresa_path = '//a[contains(@class, "topcard__org-name-link")] | /html/body/div[1]/div/section/div[2]/section/div/div[2]/div/h4/div[1]/span[1]'
                try:
                    nomeEmpresaNew = job.find_element(By.XPATH, nomeEmpresa_path).get_attribute('innerText')
                    nomeEmpresaNew = nomeEmpresaNew.strip()
                except:
                    print('Erro ", errorCount,":  fail catch nome empresa')
                    errorCount += 1
                    continue

                paginaEmpresa_path = "//a[contains(@class, 'topcard__org-name-link')]"
                try:
                    time.sleep(0.8)
                    try:
                        if WebDriverWait(driver, 1).until(
                                EC.presence_of_element_located((By.XPATH, paginaEmpresa_path))
                        ):
                            paginaEmpresaCheck = True
                            paginaEmpresaUrl = driver.find_element(By.XPATH, paginaEmpresa_path).get_attribute('href')
                            paginaEmpresaUrl2 = paginaEmpresaUrl.replace("?trk=public_jobs_topcard-org-name", "/")
                            paginaSchool = paginaEmpresaUrl2.replace("company", "school")
                    except:
                        paginaEmpresaCheck = False

                    if paginaEmpresaCheck:
                        job.find_element(By.XPATH, paginaEmpresa_path).click()
                        driver.switch_to.window(driver.window_handles[1])

                        if paginaEmpresaUrl == driver.current_url or paginaEmpresaUrl2 == driver.current_url or paginaSchool == driver.current_url:
                            numeroFuncionario_path = '//*[@id="main-content"]/section[1]/section/div/div[2]/div[2]/ul/li/div/a'
                            try:
                                try:
                                    if WebDriverWait(driver, 5).until(
                                            EC.presence_of_element_located((By.XPATH, numeroFuncionario_path))
                                    ):
                                        funcionarioCheck = True
                                except:
                                    funcionarioCheck = False

                                if funcionarioCheck:
                                    numeroFuncionarioNew = driver.find_element(By.XPATH,
                                                                               numeroFuncionario_path).get_attribute(
                                        'innerText')
                                    extractIntFuncionarios = re.findall(
                                        r"[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",
                                        numeroFuncionarioNew)
                                    for number in extractIntFuncionarios:
                                        numeroFuncionarioNew = int(number.replace(".", "").replace(",", ""))

                                else:
                                    numeroFuncionarioNew = 'N/E'
                            except:
                                print("Erro ", errorCount, ":  fail catch numero Funcionario")
                                driver.close()
                                driver.switch_to.window(driver.window_handles[0])
                                errorCount += 1
                                continue

                            numeroSeguidores_path = '//*[@id="main-content"]/section[1]/section/div/div[2]/div[1]/h3'
                            try:
                                try:
                                    if WebDriverWait(driver, 2.5).until(
                                            EC.presence_of_element_located((By.XPATH, numeroSeguidores_path))
                                    ):
                                        seguidoresCheck = True
                                except:
                                    seguidoresCheck = False

                                if seguidoresCheck:
                                    numeroSeguidoresNew = driver.find_element(By.XPATH,
                                                                              numeroSeguidores_path).get_attribute(
                                        'innerText')
                                    extractIntSeguidores = re.findall(
                                        r"[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",
                                        numeroSeguidoresNew)
                                    for number in extractIntSeguidores:
                                        numeroSeguidoresNew = int(number.replace(".", "").replace(",", ""))

                                else:
                                    numeroSeguidoresNew = 'N/E'

                            except:
                                print("Erro ", errorCount, ":  fail catch numero Seguidores")
                                driver.close()
                                driver.switch_to.window(driver.window_handles[0])
                                errorCount += 1
                                continue

                            urlEmpresa_Path = '//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[1]/dd/a'
                            try:
                                try:
                                    if WebDriverWait(driver, 2.5).until(
                                            EC.presence_of_element_located((By.XPATH, urlEmpresa_Path))
                                    ):
                                        urlEmpresaCheck = True
                                except:
                                    urlEmpresaCheck = False

                                if urlEmpresaCheck:
                                    urlEmpresaNew = driver.find_element(By.XPATH, urlEmpresa_Path).get_attribute(
                                        'innerText')
                                    urlEmpresaNew = urlEmpresaNew.strip()
                                else:
                                    urlEmpresaNew = 'N/E'

                            except:
                                print("Erro ", errorCount, ":  fail catch url empresa")
                                driver.close()
                                driver.switch_to.window(driver.window_handles[0])
                                errorCount += 1
                                continue

                            localSedeEmpresa_path = '//*[@id="main-content"]/section[1]/div/section[1]/div/dl/div[4]/dd'
                            try:
                                try:
                                    if WebDriverWait(driver, 2.5).until(
                                            EC.presence_of_element_located((By.XPATH, localSedeEmpresa_path))
                                    ):
                                        sedeEmpresaCheck = True
                                except:
                                    sedeEmpresaCheck = False

                                if sedeEmpresaCheck:
                                    localSedeEmpresaNew = driver.find_element(By.XPATH,
                                                                              localSedeEmpresa_path).get_attribute(
                                        'innerText')
                                    localSedeEmpresaNew = localSedeEmpresaNew.strip()
                                else:
                                    localSedeEmpresaNew = "N/E"
                            except:
                                print("Erro ", errorCount, ":  fail catch local sede empresa")
                                driver.close()
                                driver.switch_to.window(driver.window_handles[0])
                                errorCount += 1
                                continue

                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])

                        else:
                            print("Erro ", errorCount, ":  fail enter pagina empresa")
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            errorCount += 1
                            continue

                    else:
                        numeroFuncionarioNew = 'N/E'
                        numeroSeguidoresNew = 'N/E'
                        urlEmpresaNew = 'N/E'
                        localSedeEmpresaNew = "N/E"
                except:
                    print("Erro ", errorCount, ":  fail catch pagina empresa")
                    errorCount += 1
                    continue

                try:
                    if driver.find_elements(By.XPATH,
                                            "//button[contains(@data-impression-id, 'public_jobs_apply-link-offsite_sign-up-modal')]"):
                        driver.find_element(By.XPATH,
                                            "//button[contains(@data-impression-id, 'public_jobs_apply-link-offsite_sign-up-modal')]").click()
                        driver.find_element(By.XPATH, "//*[@id='teriary-cta-container']/a").click()
                        driver.switch_to.window(driver.window_handles[1])
                        driver.execute_script("window.stop();")
                        urlCandidaturaNew = driver.current_url
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                    else:
                        urlCandidaturaNew = urlPageNew
                except:
                    print("Erro ", errorCount, ":  fail catch url candidatura")
                    errorCount += 1

                    continue
                item += 1
                idJob.append(idJobNew)
                urlPage.append(urlPageNew)
                nomeVaga.append(nomeVagaNew)
                nomeEmpresa.append(nomeEmpresaNew)
                urlEmpresa.append(urlEmpresaNew)
                modeloContrato.append(modeloContratoNew)
                tipoContrato.append(tipoContratoNew)
                experiencia.append(experienciaNew)
                numCandidatos.append(numCandidatosNew)
                dataPostagem.append(dataPostagemNew)
                dataScrap.append(now.strftime("%d/%m/%Y %H:%M:%S"))
                numeroFuncionario.append(numeroFuncionarioNew)
                numeroSeguidores.append(numeroSeguidoresNew)
                localSedeEmpresa.append(localSedeEmpresaNew)
                urlCandidatura.append(urlCandidaturaNew)
                errorCount = 0
                break
        saveProgress()
        return True
    except:
        saveProgress()
        return False


for url in urlList:
    while True:
        try:
            driver = startWebService(url)
            jobs_num = driver.find_element(By.XPATH, "//span[contains(@class, 'results-context-header__job-count')]").get_attribute("innerText")
            if len(jobs_num.split('.')) > 1:
                jobs_num = int(jobs_num.split('.')[0]) * 1000
            else:
                jobs_num = int(jobs_num)
            jobs_num = int(jobs_num)
            getAllList(jobs_num)

            if scrapProcess(driver):
                driver.quit()
                break
        except:
            driver.quit()
            time.sleep(10)
            print("Erro: fail catch load page")
            continue

saveProgress()
print("Scrap is done")
