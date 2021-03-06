from pprint import pprint
from nbquery import NBQuery
import os


class NBQueryCLI(NBQuery):

  def __init__(self,hostname='localhost.com',
                  port=9200,
                  user='user',
                  pw='password'):

    super(NBQueryCLI, self).__init__(hostname,port,user,pw)

  def _make_fs_safe_link(self, link):
    fs_safe_link = link.replace("/","_")
    fs_safe_link = fs_safe_link.split("?")[0]
    if not fs_safe_link.endswith('html'):
      fs_safe_link += ".html"
    return fs_safe_link

  def _save_files(self,html_contents,path):
    
    for html_content in html_contents:
      print "Saving Articles..%s" % html_content["source_link"]

      save_path = os.path.join(
        path, self._make_fs_safe_link(html_content["source_link"]))
      #link_split = html_content["source_link"].split(".")
      #fs_safe_link = html_content["source_link"].replace("/","_")

      #if link_split[-1] == "html":
      #  save_path = os.path.join(path, html_content["source_link"].replace("/","_")) 
      #else:
      #  save_path = os.path.join(path, html_content["source_link"].replace("/","_") + ".html") 

      html_output = open(save_path, "w")
      html_output.write(html_content["html_content"].encode('utf-8').strip())
      html_output.close()

  def get_html_source(self,source,path,limit):
    if not os.path.exists(path):
        os.makedirs(path)
    results = self.search(source=source,projections=["title","html_content","source_link"],limit=limit)
    self._save_files(results,path)

if __name__ == "__main__":
  pass
  #nb_cli = NBQueryCLI("island2.cs.columbia.edu")
  #nb_cli.get_html_source("www.nytimes.com*","/tmp/",100)


