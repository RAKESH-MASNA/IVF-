/*******DATA CLEANING***********/
DESCRIBE ivf_equipment_master;
DESCRIBE ivf_equipment_utilization;

SELECT COUNT(*) FROM ivf_equipment_master;
SELECT COUNT(*) FROM ivf_equipment_utilization;
/********************************************************************************************/
# CHECKING NULL VALUES FOR 1-DATASET
SELECT
	SUM(equipment_id IS NULL) AS null_equipment_id,
    SUM(equipment_type IS NULL) AS null_equipment_type,
    SUM(installation_date IS NULL) AS null_installation_date,
    SUM(is_critical_for_procedure IS NULL) AS null_is_critical_for_procedure,
    SUM(lab_id IS NULL) AS null_lab_id,
    SUM(manufacturer IS NULL) AS null_manufacturer,
    SUM(model IS NULL) AS null_model
FROM ivf_equipment_master;

# CHECKING NULL VALUES FOR 2-DATASET
SELECT
    SUM(lab_id is NULL) AS null_lab_id,
    SUM(equipment_id IS NULL) AS null_equipment_id,
    SUM(equipment_type IS NULL) AS null_equipment_type,
	SUM(max_capacity_hrs IS NULL) AS null_max_capacity_hrs,
    SUM(utilization_hrs IS NULL) AS null_utilization_hrs, 
    SUM(utilization_pct IS NULL) AS null_utilization_pct,
    SUM(idle_hrs IS  NULL )AS null_idle_hrs,
    SUM(technical_downtime_hrs IS NULL) AS null_technical_downtime_hrs,
    SUM(planned_maintenance_hrs IS NULL) AS null_planned_maintenance_hrs,
    SUM(workflow_delay_events IS NULL) AS null_workflow_delay_events,
    SUM(avg_delay_minutes IS NULL IS NULL)AS null_avg_delay_minutes,
    SUM(primary_procedure IS NULL) AS null_primary_procedure,
    SUM(redundancy_available IS NULL) AS null_redundancy_available,
    SUM(total_cases_day_lab IS NULL) AS null_total_cases_day_lab
FROM ivf_equipment_utilization;

/* IF YOU FIND ANY NULL VALUE YOU CAN REPLACE WITH MEAN FOR EXAMP*/
UPDATE ivf_equipment_utilization
SET total_cases_day_lab =
(
    SELECT AVG(total_cases_day_lab)
    FROM ivf_equipment_utilization
)
WHERE total_cases_day_lab IS NULL;
/********************************************************************************************/


/********************************************************************************************/
/***********HANDLING DUPLICATES***********/
/*1-DATASET*/

SELECT
	lab_id,
    equipment_id,
	equipment_type,
    manufacturer,
    model,
    installation_date,
    is_critical_for_procedure,
    COUNT(*) AS CNT
FROM ivf_equipment_master
GROUP BY lab_id,equipment_id,equipment_type,manufacturer,model,installation_date,is_critical_for_procedure
HAVING COUNT(*)>1;

/*2-DATASET*/
SELECT
	date,
    lab_id,
    equipment_id,
    equipment_type,
    max_capacity_hrs,
    utilization_hrs,
    utilization_pct,
    idle_hrs,
    technical_downtime_hrs,
    planned_maintenance_hrs,
    workflow_delay_events,
    avg_delay_minutes,
    primary_procedure,
    redundancy_available,
    total_cases_day_lab,
    COUNT(*) AS CNT
FROM ivf_equipment_utilization
GROUP BY date,lab_id,equipment_id,equipment_type,max_capacity_hrs,utilization_hrs,utilization_pct,idle_hrs,
technical_downtime_hrs,planned_maintenance_hrs,workflow_delay_events,avg_delay_minutes,primary_procedure,
redundancy_available,total_cases_day_lab
HAVING COUNT(*)>1;

CREATE TABLE ivf_equipment_utilization_backup AS
SELECT * FROM ivf_equipment_utilization;

DELETE FROM ivf_equipment_utilization
WHERE (date, lab_id, equipment_id, equipment_type, max_capacity_hrs,
       utilization_hrs, utilization_pct, idle_hrs,
       technical_downtime_hrs, planned_maintenance_hrs,
       workflow_delay_events, avg_delay_minutes,
       primary_procedure, redundancy_available, total_cases_day_lab)
IN (
    SELECT date, lab_id, equipment_id, equipment_type, max_capacity_hrs,
           utilization_hrs, utilization_pct, idle_hrs,
           technical_downtime_hrs, planned_maintenance_hrs,
           workflow_delay_events, avg_delay_minutes,
           primary_procedure, redundancy_available, total_cases_day_lab
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                   PARTITION BY
                       date, lab_id, equipment_id, equipment_type,
                       max_capacity_hrs, utilization_hrs, utilization_pct,
                       idle_hrs, technical_downtime_hrs,
                       planned_maintenance_hrs, workflow_delay_events,
                       avg_delay_minutes, primary_procedure,
                       redundancy_available, total_cases_day_lab
                   ORDER BY date
               ) AS rn
        FROM ivf_equipment_utilization
    ) t
    WHERE rn > 1
);
SET SQL_SAFE_UPDATES = 0;
/********************************************************************************************/


/********************************************************************************************/
/*********TYPE CASTING************/
/* 1-DATASET */
SELECT DISTINCT installation_date
FROM ivf_equipment_master;
UPDATE ivf_equipment_master
SET installation_date =
STR_TO_DATE(installation_date, '%d-%m-%Y');

SELECT installation_date
FROM ivf_equipment_master
LIMIT 5;


SELECT DISTINCT is_critical_for_procedure
FROM ivf_equipment_master;
UPDATE ivf_equipment_master
SET is_critical_for_procedure =
CASE
    WHEN UPPER(is_critical_for_procedure) IN ('TRUE', 'YES', 'Y', '1') THEN 1
    ELSE 0
END;


ALTER TABLE ivf_equipment_master
MODIFY lab_id VARCHAR(50),
MODIFY equipment_id VARCHAR(50),
MODIFY equipment_type VARCHAR(50),
MODIFY manufacturer VARCHAR(100),
MODIFY model VARCHAR(100),
MODIFY installation_date DATE,
MODIFY is_critical_for_procedure BOOLEAN;

DESCRIBE ivf_equipment_master;

/* 2-DATASET */

/*DATE*/
SELECT COUNT(*) AS empty_dates
FROM ivf_equipment_utilization
WHERE date = '';

UPDATE ivf_equipment_utilization
SET date = NULL
WHERE date = '';

UPDATE ivf_equipment_utilization
SET date = STR_TO_DATE(date, '%d-%m-%Y')
WHERE date IS NOT NULL
  AND date <> '';

SELECT DISTINCT date
FROM  ivf_equipment_utilization
LIMIT 10;

ALTER TABLE ivf_equipment_utilization
MODIFY date DATE;

SELECT date 
FROM ivf_equipment_utilization;

/* BOOLEAN*/
SELECT redundancy_available
FROM ivf_equipment_utilization;
UPDATE ivf_equipment_utilization
SET redundancy_available =
CASE
    WHEN UPPER( redundancy_available) IN ('TRUE', 'YES', 'Y', '1') THEN 1
    ELSE 0
END;

ALTER TABLE ivf_equipment_utilization
MODIFY date DATE,
MODIFY lab_id VARCHAR(50),
MODIFY equipment_id VARCHAR(50),
MODIFY equipment_type VARCHAR(50),
MODIFY max_capacity_hrs INT,
MODIFY utilization_hrs DECIMAL(10,2),
MODIFY utilization_pct DECIMAL(5,2),
MODIFY idle_hrs DECIMAL(10,2),
MODIFY technical_downtime_hrs INT,
MODIFY planned_maintenance_hrs DECIMAL(10,2),
MODIFY workflow_delay_events INT,
MODIFY avg_delay_minutes DECIMAL(10,2),
MODIFY primary_procedure VARCHAR(50),
MODIFY redundancy_available BOOLEAN,
MODIFY total_cases_day_lab INT;

DESCRIBE ivf_equipment_utilization;
/********************************************************************************************/


/********************************************************************************************/
/***********OUTLYER ANALYSIS************/
/* Method 1 - IQR*/
WITH ordered_data AS(
	SELECT total_cases_day_lab,
		ROW_NUMBER() OVER (ORDER BY total_cases_day_lab) AS rn,
		COUNT(*) OVER() AS total_rows
	FROM ivf_equipment_utilization
)
SELECT
	MAX(CASE WHEN rn = FLOOR(0.25 * (total_rows+1))THEN total_cases_day_lab END) AS Q1,
    MAX(CASE WHEN rn = FLOOR(0.75 * (total_rows+1))THEN total_cases_day_lab END) AS Q3
FROM  ordered_data;
		
WITH STATS AS (
	SELECT
    	MAX(CASE WHEN rn = FLOOR(0.25 * (total_rows+1))THEN total_cases_day_lab END) AS Q1,
		MAX(CASE WHEN rn = FLOOR(0.75 * (total_rows+1))THEN total_cases_day_lab END) AS Q3
	FROM (
    	SELECT total_cases_day_lab,
		ROW_NUMBER() OVER (ORDER BY total_cases_day_lab) AS rn,
		COUNT(*) OVER() AS total_rows
	FROM ivf_equipment_utilization
    )t
)
SELECT * 
FROM ivf_equipment_utilization,STATS
WHERE total_cases_day_lab < (Q1 - 1.5*(Q3-Q1))
or	  total_cases_day_lab > (Q1 + 1.5*(Q3-Q1));
/********************************************************************************************/


/********************************************************************************************/
/***ZEO AND NEAR ZERO VARIANCE****/
/* ZERO VARIANCE*/
SELECT 
	MIN(redundancy_available) AS MIN_VAL,
    MAX(redundancy_available) AS MAX_VAL
FROM ivf_equipment_utilization;

SELECT
	COUNT(DISTINCT redundancy_available) AS DISTINCT_VAL
FROM  ivf_equipment_utilization;
/***NEAR ZERO VARIANC***/
SELECT
    STDDEV_POP(redundancy_available) AS std_dev
FROM ivf_equipment_utilization;

SELECT
	COUNT(DISTINCT redundancy_available) AS DISTINCT_VAL
FROM  ivf_equipment_utilization;

/***THE ABOVE COLOUMN IS NZ****/
/********************************************************************************************/

/*********************************************************************************************/
/********DISCRETIZATION***********/
SELECT
	total_cases_day_lab,
    CASE
		WHEN total_cases_day_lab BETWEEN 0 AND 10 THEN 'LOW'
		WHEN total_cases_day_lab BETWEEN 10 AND 20 THEN 'MEDIUM'
		ELSE 'HIGH'
	END AS total_case_category
FROM ivf_equipment_utilization;

/*2-METHOD*/
SELECT
	 utilization_pct,
     CASE
		WHEN  utilization_pct < 50 THEN 'UNDERUTILIZED'
        WHEN  utilization_pct BETWEEN 50 AND 80 THEN 'OPTIMAL'
        ELSE 'OVERUTILIZED'
	END  AS  utilization_pct_cat
FROM ivf_equipment_utilization;

/***METHOD 3: DISCRETIZE DOWNTIME HOURS***/
SELECT
	technical_downtime_hrs,
    CASE
		WHEN technical_downtime_hrs = 0 THEN 'NO DOWNTIME'
        WHEN technical_downtime_hrs BETWEEN 1 AND 3 THEN 'LOW'
        ELSE 'HIGH'
	END AS technical_downtime_hrs_cat
FROM ivf_equipment_utilization;
/***************************************************************************************/

/***************************************************************************************/
/******FEATURE SCALING***********/
/*Min-Max Scaling*/
/*utilization_pct*/
SELECT 
	utilization_pct,
    (utilization_pct - stats.min_val)/
    (stats.max_val - stats.min_val) AS Scaled_utilization_pct
FROM ivf_equipment_utilization
CROSS JOIN(
	SELECT
    MIN(utilization_pct) AS min_val,
    MAX(utilization_pct) AS max_val
    FROM ivf_equipment_utilization
) stats;
    
/*utilization_hrs*/
SELECT 
	utilization_hrs,
    (utilization_hrs - stats.min_val)/
    (stats.max_val - stats.min_val) AS Scaled_utilization_hrs
FROM ivf_equipment_utilization
CROSS JOIN(
	SELECT
    MIN(utilization_hrs) AS min_val,
    MAX(utilization_hrs) AS max_val
    FROM ivf_equipment_utilization
) stats;

/*idle_hrs*/
SELECT 
	idle_hrs,
    (idle_hrs- stats.min_val)/
    (stats.max_val - stats.min_val) AS Scaled_idle_hrs
FROM ivf_equipment_utilization
CROSS JOIN(
	SELECT
    MIN(idle_hrs) AS min_val,
    MAX(idle_hrs) AS max_val
    FROM ivf_equipment_utilization
) stats;

/*avg_delay_minutes*/
SELECT 
	 avg_delay_minutes,
    (avg_delay_minutes- stats.min_val)/
    (stats.max_val - stats.min_val) AS Scaled_idle_hrs
FROM ivf_equipment_utilization
CROSS JOIN(
	SELECT
    MIN(avg_delay_minutes) AS min_val,
    MAX(avg_delay_minutes) AS max_val
    FROM ivf_equipment_utilization
) stats;

/** STADADIZE SCALING**/
/***(X-MEAN)/STD.D)***/

/** STADADIZE SCALING**/
/***(X-MEDIAN(X))/IQR(X))***/
/***************************************************************************/
