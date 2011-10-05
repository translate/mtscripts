#--- Preparing Moses corpus ----#

langtag1='zu'
langtag2='xh'
corpusname='corpus'
datadir='data'
mosesdir='moses'

server='indlovu.local'
servpaths=('/var/samba/public/mt-work/translations/4.reviewed' '/var/samba/public/mt-work/alignment/4.reviewed')
srcpaths=()
locpath='/home/laurette/Translate_org_za/trunk/mtscripts'
segmentdir='segdata'
filetype='po' #only one file type is assumed

# Switches for stages
useserver=true
posegment=false
pocount=true
mosesconvert=true
buildmodel=true

#---- Building Moses model ----#

mosespath='/home/laurette/Translate_org_za/Moses'
workdir=work_5Oct
datadir=data_5Oct
corpuspath=$locpath/$mosesdir/corpus
tunetag='tune_'
tunecorpus=$tunetag$(echo $corpusname)
testtag='test_'
testcorpus=$testtag$(echo $corpusname)

# Switches for building

tuning=true