# FUNCTION DEFINITION
def vcfgz_to_gz(vcf_gz_file, vcf_name = "my_vcf.vcf", csv_file = "my_snps.csv"):
    '''This function processes a vcf.gz file using the gzip and shutil packages.
    gzip is used to unpackage the .gz compressed file format.  (shutil provides
    file handling functions.'''
    # Processing cell 1
    import gzip
    import shutil

    print("converting your vcf.gz file to .vcf.")
    with gzip.open(vcf_gz_file, 'rb') as f_in:
        with open(vcf_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

# FUNCTION DEFINITION
def vcf_to_df(vcf_file,csv_file = "my_snps.csv"):
    '''This function processes a .vcf using the StringIO, and re packages.
     StringIO allows the lines of the .vcf file to be loaded into memory.
     re is used to do some processing on the file, which is then saved as a
     temporary .txt file.  Loading the .txt file into pandas removes the
     metadata and provides a pandas dataframe '''

    print("loading necessary packages")
    # import libraries and modules
    ## StringIO: tools for working iwth strings
    from io import StringIO

    ## re: regular expressions (find and replace patterns)
    import re

    ## pandas for dataframe
    import pandas as pd

    import shutil

    print("Make sure you're working with a .vcf not .vcf.gz file")
    print("Opening your VCF file")
    file1 = open(vcf_file, 'r')

    print("Reading the lines of the file into a python list")
    vcf_in_list = file1.readlines()

    print("Processing the vcf; this may take a minute")
    # process vcf file
    ## loop over list
    for i in range(0,len(vcf_in_list)):

        # get current row
        row_i = vcf_in_list[i]

        # turn "##" comments in vcf file into "#" comments for python
        row_i = re.sub(r"^##", "#", row_i)

        # remove the "#" from infront of row with CHROM
        ## so it isn't commented out
        row_i = re.sub(r"^#CHROM", "CHROM", row_i)

        # store cleaned list
        vcf_in_list[i] = row_i

    print("Saving the processed vcf file as a temporary .txt file")
    # create file to store output
    with open("vcf_temp.txt", 'w') as file:
            # loop over list
            for row in vcf_in_list:

                # do something....
                vcf_in_list = "".join(map(str, row))

                #store in the file
                file.write(vcf_in_list)

    print("Reading your vcf data as a Pandas file without metadata")
    # read in file back in using pandas
    ## set comment character as "#"
    ## so it all gets skipped
    import pandas as pd
    my_snps = pd.read_csv("vcf_temp.txt",
                    sep='\t',
                    lineterminator='\n',
                    comment = "#")
    print("Saving your dataframe as a .csv for backup.  Download this from Colab or else it will disappear : (")
    my_snps.to_csv(csv_file,
               index=False)

    print("Done! \n\n If you're not finding your dataframe, make sure defined a variable to hold the output of the function")

    return(my_snps)


def phased_to_featurized(df):
    df_shape = df.shape
    df_nrows = df_shape[0]
    df_ncols = df_shape[1]
    df_cols= df.columns
    df_working = df

    print("sorry, this is slow...sometimes really slow...you may want to go get some coffee or tea...")
    for i in range(0,df_ncols):
        if i == 1000:
            print("1000 individuals processed, 1500 to go : )")
        if i == 2000:
            print("1000 individuals processed, 500 to go : )")
        df_working[df_cols[i]][df_working[df_cols[i]] == "0|0"] = 0
        df_working[df_cols[i]][df_working[df_cols[i]] == "1|1"] = 2
        df_working[df_cols[i]][df_working[df_cols[i]] == "1|0"] = 1
        df_working[df_cols[i]][df_working[df_cols[i]] == "0|1"] = 1



    print("Done!")
    return(df_working)


# def drop_metadata()


#def keep_biallelic(snp_df):
#    import pandas as pd
#    real_SNPs = ["A","T","C","G"]
#    onlyATCG_REF = snp_df.REF.isin(real_SNPs)
#    onlyATCG_ALT = snp_df.ALT.isin(real_SNPs)
#    phased_snps_biallelic = snp_df[onlyATCG_REF]
#    phased_snps_biallelic = phased_snps_biallelic[onlyATCG_ALT]
#
#    return(phased_snps_biallelic)