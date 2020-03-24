#/bin/bash
# Force termination of all the Terminating sesions
# Works on a per-region basis

TERMINATING_SESSIONS=`aws ssm describe-sessions --state History --filters "key=Status, value=Terminating" --query "Sessions[].SessionId" --output text`

for terminating_session in ${TERMINATING_SESSIONS}; do
	echo "Force session termination of ${terminating_session}"
	aws ssm terminate-session --session-id ${terminating_session}
done
