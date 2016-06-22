import os, time, re

#################################    GLOBAL PARAMETERS    #####################################

refGenome = '/uz/data/avalok/symbiosys/gcpi_r_kul_thierry_voet/jhaan0/humangenome/fasta/hg19Mt.fa'
binaryPath = '/cm/shared/apps/'
javaPath = '/cm/shared/apps/jdk/1.7.0/bin/java'
picardPath = '/cm/shared/apps/picard/current/'
gatkPath = '/cm/shared/apps/gatk/current/'
bedtoolsPath = '/cm/shared/apps/bedtools/2.17.0/bin/'
localBinaryPath = '/home/dbrown0/miniconda3/envs/py2bioinf/bin/'
tmpDir = ''

#################################    BEGIN COMMANDS    #####################################

def runJob(comm, taskName):
    '''An internal function used by the rest of the functions to spawn a process in the shell, 
    run a command based on the value of the string "comm" and capture the standard output.
    Throws an exception when failure occurs'''
    started = time.strftime('%X %x %Z')
    print('\n##############################################    RUNNNG TASK ' + taskName + ' at {0}'.format(started) +   '    ###############################################')
    print(comm + '\n')
    #run the command. Comment out the line below to print only the command and not run it.
    os.system(comm)
    
    
def trimReads(inputFile, outputFile):
    'Take the raw sequencing reads and trim off first 12 bases of sequence'
    read2 = re.sub('.R1.fastq.gz', '.R2.fastq.gz', inputFile)
    outputFile2 = re.sub('.R1.', '.R2.', outputFile)
    comm = '''{0}cutadapt -u 12 \
    -o {3} -p {4} {1} {2} \
    '''.format(localBinaryPath, inputFile, read2, outputFile, outputFile2)
    runJob(comm, 'TRIMMING READS')
    

def generateSamindex(inputFile, outputFile):
    '''Generate the indexes of the reads needed for alignment with bwa'''
    #	Extract the read 2 filename
    read2 = re.sub('.R1.', '.R2.', inputFile)
    outputFile2 = re.sub('.R1.', '.R2.', outputFile)
    comm1 = '''{0}bwa/0.6.2/bwa aln -l 32 {1} {2} > {3} \
    '''.format(binaryPath, refGenome, inputFile, outputFile)
    
    comm2 = '''{0}bwa/0.6.2/bwa aln -l 32 {1} {2} > {3} \
    '''.format(binaryPath, refGenome, read2, outputFile2)
    runJob(comm1, 'GENERATING INDEX 1')
    runJob(comm2, 'GENERATING INDEX 2')
    
    
def alignReads(indexFile, inputFile, outputFile):
    '''Align the fastq reads using bwa'''
    #	Extract the index 2 filename
    index2 = re.sub('.R1.', '.R2.', indexFile)
    #	Extract the read 2 filename
    read2 = re.sub('.R1.', '.R2.', inputFile)
    
    # Extract names for the read group information
    m = re.search('GC03(.+?)_', inputFile)
    if m:
        runName = 'GC03' + m.group(1)
    m = re.search('{0}(.+?).16'.format(runName), inputFile)
    if m:
        sampleName = m.group(1)
    #   Build the read group information
    rgID = '@RG\tID:{0}\tSM:{1}\tPL:ILLUMINA\tLB:{1}'.format(runName, sampleName)
    
    #   Build the command for alignment
    comm = '''{0}bwa/0.6.2/bwa sampe -P -r {1} \
    -s {2} {3} {4} {5} {6} \
    | {0}samtools/current/samtools view -bS -o {7} -S \    
    '''.format(binaryPath, rgID, refGenome, indexFile, index2, inputFile, read2, outputFile)
    runJob(comm, 'ALIGNING READS')
    
    
def mergeBamPipeline(inputFileNames, outputFile):
    'As some samples are split over 4 lanes of sequencing on a NextSeq combine the aligned files'
    bam1 = inputFileNames[0]
    bam2 = inputFileNames[1]
    bam3 = inputFileNames[2]
    bam4 = inputFileNames[3]
    comm = '''java -Xmx5g -jar {0}MergeSamFiles.jar \
    INPUT={1} INPUT={2} INPUT={3} INPUT={4} \
    OUTPUT={5} SORT_ORDER=coordinate CREATE_INDEX=true \
    '''.format(picardPath, bam1, bam2, bam3, bam4, outputFile, tmpDir)
    runJob(comm, 'MERGING BAM FILES')
    
    
def sortSamtools(inputFile, outputFile):
    comm = "{0}samtools/current/samtools sort {1} > {2}".format(binaryPath, inputFile, outputFile)
    runJob(comm, "SORTING ALIGNMENTS")
    

def indexSamtools(inputFile):
    com = "{0}samtools/current/samtools index {1}".format(binaryPath, inputFile)
    # No output file therefore invoke os.system directly
    print('\n##############################################    RUNNNG TASK INDEX SAMTOOLS     ###############################################\n')
    os.system(com)
    
    
def estimateLibComplexity(inputFile, outputFile):
    'Estimate the library size using Picard tools. This should be done before duplicate removal'
    comm = '''java -Xmx5g -jar {0}EstimateLibraryComplexity.jar \
     I={1} \
     O={2}'''.format(picardPath, inputFile, outputFile)
    runJob(comm, 'ESTIMATING LIBRARY SIZE')
    
