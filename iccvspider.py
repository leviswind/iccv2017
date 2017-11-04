import os
import re
import urllib


def get_pdf_sites(gen_site):
    pdf_cp = re.compile(r'<a href="(.*)">pdf')
    title_cp = re.compile(r'\ntitle = {(.*)')
    sup_cp = re.compile(r'<a href="(.*)">supp')
    contents = urllib.urlopen(gen_site).read()
    pdf_sites = pdf_cp.findall(contents)
    sup_sites = sup_cp.findall(contents)
    titles = title_cp.findall(contents)
    titles = [title.split('}')[0] for title in titles]
    for i, title in enumerate(titles):
        for ch in ["\\", "/", ':', '?', '<', '>', '|', '\"', '\r']:
            title = title.replace(ch, "")
        titles[i] = title
        print title
    kv = {k.split('/')[-1][:-10]: v for k, v in zip(pdf_sites, titles)}
    return pdf_sites, sup_sites, titles, kv


def save_sites(save_dir, sites, titles):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for i, site in enumerate(sites):
        savefw = save_dir + titles[i]
        print savefw, '\t', i
        if os.path.exists(savefw):
            continue
        with open(savefw, 'wb') as f:
            f.write(urllib.urlopen(site).read())


if __name__ == '__main__':
    pdf_sites, sup_sites, pdf_titles, kv = get_pdf_sites('http://openaccess.thecvf.com/ICCV2017.py')
    sup_titles = [kv[title.split('/')[-1][:-17]] + '_supplemental.pdf' for title in sup_sites]
    pdf_titles = [title + '.pdf' for title in pdf_titles]
    pdf_sites = ['http://openaccess.thecvf.com/' + site for site in pdf_sites]
    sup_sites = ['http://openaccess.thecvf.com/' + site for site in sup_sites]
    save_sites('./pdf/', pdf_sites, pdf_titles)
    save_sites('./supp/', sup_sites, sup_titles)
