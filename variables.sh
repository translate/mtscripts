#--- Preparing Moses corpus ----#

langtag1='zu'
langtag2='xh'
corpusname='corpus'
datadir='data'
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

mosespath='/home/laurette/Translate.org.za/Moses' #directory containing tools/ (as explained in the online step-by-step guide)
system='i686-m64'
order=3 #length of ngrams
bworkdir=work_5Oct
bdatadir=data_5Oct
corpuspath=$locpath/$mosesdir/corpus #the location from which to get the data and throw into bdatadir
tunetag='tune_'
tunecorpus=$tunetag$(echo $corpusname)
testtag='test_'
testcorpus=$testtag$(echo $corpusname)
installdate='20110627-1042'

# Switches for building

getdata=false
testing=false
tuning=true
