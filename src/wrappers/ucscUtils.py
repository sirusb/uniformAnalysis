#!/usr/bin/env python2.7
# ucscUtils.py module holds methods for running various utilities from the kent/src tree in
# a LogicalStep.
#
# Runs from (in path) tools dir symlinks
# NOTE: fastqStatsAndSubsample needs to be added to ucscUtils package and symlinked!!!

def version(step, logOut=True, tool=None):
    '''Returns tool version.  Will log to stepLog unless requested not to.'''
    if tool != None:
        toolName = tool
        return step.getToolVersion(toolName, logOut)
    toolName = __name__.split('.')[-1]
    version = "unversioned"  # Sorry, this tool has no version.
    if logOut:
        step.log.out("# "+toolName+" [version: " + version + "]")
    return version

def bedGraphToBigWig(step, inBedGraph, outBigWig):
    '''Converts a bedGraph to a bigWig.'''
    
        # "bedGraphToBigWig input.tmp chromLengths output.bigWig"
    cmd = 'bedGraphToBigWig {bedGraph} {chromInfo} {bigWig}'.format( bedGraph=inBedGraph, \
          chromInfo=step.ana.getSetting(step.ana.genome+'ChromInfoFile'), \
          bigWig=outBigWig)
          
    toolName = __name__.split('.')[-1] + " bedGraphToBigWig"
    step.toolBegins(toolName)
    step.getToolVersion('bedGraphToBigWig', logOut=True)

    step.err = step.ana.runCmd(cmd, logOut=False, log=step.log)
    step.toolEnds(toolName,step.err)

def fastqStatsAndSubsample(step, inFastq, simpleStats, sampleFastq):
    '''Sample a fastq.'''
    
    cmd = 'fastqStatsAndSubsample -sampleSize={reads} -seed={seed} {input} {outStats} {outSample}'.format( \
          reads='{sample}',seed=step.ana.getSetting('fastqSampleSeed', '12345'), \
          input=inFastq, outStats=simpleStats, outSample=sampleFastq)
    
    sampleSize = int( step.ana.getSetting('fastqSampleReads','100000') )
      
    toolName = __name__.split('.')[-1] + ' fastqStatsAndSubsample'
    step.toolBegins(toolName)
    step.getToolVersion('fastqStatsAndSubsample', logOut=True)

    #step.err = step.ana.runCmd(cmd, log=step.log) # stdout goes to file
    while sampleSize >= 40000:
        step.err = step.ana.runCmd(cmd.format(sample=sampleSize), log=step.log)
        if step.err != 65280: # size error
            break;
        sampleSize = sampleSize - 15000
        
    step.toolEnds(toolName,step.err)
    
def edwBamStats(step, inBam, statsRa, outSample, sampleSize):
    '''Bam evaluation statistics.'''
    
    cmd = 'edwBamStats {bamIn} {raOut} -sampleBed={outBed} -sampleBedSize={size}'.format( \
          bamIn=inBam, raOut=statsRa, outBed=outSample, size=sampleSize)
      
    toolName = __name__.split('.')[-1] + ' edwBamStats'
    step.toolBegins(toolName)
    step.getToolVersion('edwBamStats', logOut=True)

    step.err = step.ana.runCmd(cmd, log=step.log) # stdout goes to file
    step.toolEnds(toolName,step.err)
