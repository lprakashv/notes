# Big Data

## The four Vs

!!! info "AI-generated"

“Big data” is a relative engineering description, not a fixed byte threshold. It
is often summarized with four Vs:

1. **Volume:** the amount of data exceeds the convenient capacity of one machine
   or one conventional database design.
2. **Velocity:** data arrives or must be processed quickly.
3. **Variety:** sources and formats differ.
4. **Veracity:** quality, meaning, and trustworthiness vary.

The useful question is which constraint forces a distributed design. Distribution
adds network, consistency, recovery, and operational costs, so a single database
or machine is preferable while it still meets the requirement.

## Hadoop

!!! info "AI-generated"

Apache Hadoop emerged in the mid-2000s from the Nutch project, influenced by
Google's papers on the Google File System and MapReduce. It provides distributed
storage and batch processing on clusters of commodity machines.

Consists of:

1. HDFS - Distributed File System
2. YARN - Yet another resource manager, manages all nodes, assigns tasks to nodes etc.
3. Map-Reduce - allows you to write scripts to analyze data that is spread across multiple machines.

## Vendor history

!!! info "AI-generated"

Hortonworks and Cloudera were prominent commercial Hadoop distributors. They
completed a merger in 2019, so treating them as two current competing vendors is
historical rather than a present-day market comparison.

### Hortonworks

!!! info "AI-generated"

Hortonworks Data Platform (HDP) bundled Hadoop ecosystem projects. Hortonworks
DataFlow (HDF) focused on data-in-motion tooling, including Apache NiFi.

### Cloudera

!!! info "AI-generated"

Cloudera combined open-source ecosystem projects with commercial management,
security, governance, and support. Current product names and packaging change;
check vendor documentation before using these historical names in an architecture.
