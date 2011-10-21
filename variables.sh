#--- Preparing Moses corpus ----#

langtag1='zu'
langtag2='xh'
corpusname='corpus'
datadir='adata'
mosesdir='moses'

server='indlovu.local'
servpaths=('/var/samba/public/mt-work/translations/4.reviewed' '/var/samba/public/mt-work/alignment/4.reviewed')
srcpaths=()
locpath='/home/laurette/Translate.org.za/trunk/mtscripts'
segmentdir='segdata'
filetype='po' #only one file type is assumed

# Switches for stages
useserver=true
posegment=false
pocount=true
mosesconvert=false
buildmodel=false

#---- Building Moses model ----#

mosespath='/home/laurette/Translate.org.za/Moses'
bworkdir=work_5Oct
bdatadir=data_5Oct
corpuspath=$locpath/$mosesdir/corpus
tunetag='tune_'
tunecorpus=$tunetag$(echo $corpusname)
testtag='test_'
testcorpus=$testtag$(echo $corpusname)
installdate='20110627-1042'

# Switches for building

tuning=true
