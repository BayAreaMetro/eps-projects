--- Data Loads Log Table Creation ---


CREATE TABLE "admin"."data_loads_log" (
    schemaname character varying(256) ENCODE zstd,
    starttime timestamp without time zone ENCODE zstd,
    endtime timestamp without time zone ENCODE zstd,
    numrowsbefore integer ENCODE zstd,
    numrowsafter integer ENCODE zstd,
    numcolumns integer ENCODE zstd, 
    datasource character varying(256) ENCODE zstd,
    tableappended character varying(256) ENCODE zstd,
    description character varying(256) ENCODE zstd,  --may change on type/length of description
    platform character varying(256) ENCODE zstd,
    jobnumber character varying(256) ENCODE zstd
)
