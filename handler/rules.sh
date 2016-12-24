#!/usr/bin/env sh
curl -H "Content-Type: application/json" -d '{"matcher": ".*", "value": 1, "analysis_key": "viperData", "rule_key":"proof_of_concept"}' http://pit:5000/rule
