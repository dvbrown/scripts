# Idenitfying deletions from mitochondrial DNA

Mitochondrial DNA is different ot genomic DNA in many respects. An individual cell can have many mitochondiral genomes with different genotypes.  This makes tradiitional structural variant tools less than ideal.

The input for this pipeline is a pindel configuration file listing the filenames of the bamfiles to be analysed in the current directory.
The output of the pipeline is a tab delimited text file describing the deleted mitochondrial DNA segments in each sample.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisities

You will need:
```
A python installation. This pipeline has been designed with python 2.7.
```
```
The ruffus pipeline library for python "http://www.ruffus.org.uk/"
```
```
The pandas library for manipulating tables in python "http://pandas.pydata.org/"
```
I personally use the Anaconda distribution of python which comes with these modules already installed.  https://www.continuum.io/downloads
```
Pindel "http://gmt.genome.wustl.edu/packages/pindel/"
```
```
GATK "https://www.broadinstitute.org/gatk/"
```

### Installing

The pipeline code is available from github. Copy and paste this command if you have github command line tool installed: 
```
"git clone https://github.com/dvbrown/Pipelines/tree/master/Ruffus_python/160306_mtDNApipelines"
```
Alternatively you can use the github website and clone to your computer using a graphical user interface.

End with an example of getting some data out of the system or using it for a little demo

## Configuring global parameters for the pipeline
The paths to various software need to be set at the very top of the pindel_commands.py file.

```
Path to reference genome
```
```
Path to folder containing pindel executables
```
```
Path to GATK jar file
```

## Preparing files prior to running the pipeline

The bamfiles used in the pipeline should be processed with an aligner that can assign secondary alignments. BWA or MOSAIK are the best choices.
Preprocessing of these bamfiles by GATK local realignment is recommended.
The reference genome file also needs to be prepared so GATK can utilize it.

Preparing a fasta sequence dictionary
```
java -jar CreateSequenceDictionary.jar R= ref.fasta O= ref.dict
```

Preparing a fasta index
```
samtools faidx ref.fasta 
```

### Running the pipeline

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* Dropwizard - Bla bla bla
* Maven - Maybe
* Atom - ergaerga

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc