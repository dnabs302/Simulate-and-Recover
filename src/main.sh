cd "$(dirname "$0")"

echo "Running simulateAndRecovery..."
python3 "simulateAndRecovery.py"

if [ $? -eq 0 ]; then
    echo "All iterations ran successfully!"
else
    echo "Some iterations failed. Check the output above."
fi