from cx_Freeze import setup, Executable

includes = ['scrapy', 'Tkinter', 'pkg_resources', 'lxml.etree', 'lxml._elementpath']

build_options = {
                'compressed' : True,
                'optimize' : 2,
                'namespace_packages' : ['zope', 'scrapy','Tkinter', 'pkg_resources'],
                'includes' : includes,
                'excludes' : []
                }

executable = Executable(
                        script='run.py',
                        copyDependentFiles=True,
                        includes=includes
                        )

setup(name='Inventory Scraper',
      version='0.1',
      description='Scrapes wine inventories!',
      options= {'build_exe': build_options},
      executables=[executable])