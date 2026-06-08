#!/bin/bash
# Install the X post scheduler as a cron job.
# Runs every Tuesday at 9:00 AM, posts the next blog from the queue.
#
# Usage: bash scripts/install_cron.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
POST_SCRIPT="$SCRIPT_DIR/post_x.py"
LOG_FILE="$SCRIPT_DIR/.x_posted.log"

if [[ ! -f "$POST_SCRIPT" ]]; then
    echo "ERROR: $POST_SCRIPT not found"
    exit 1
fi

# Build the crontab line
CRON_LINE="0 9 * * 2 /usr/bin/env python3 $POST_SCRIPT post >> $LOG_FILE 2>&1"

# Check if already installed
if crontab -l 2>/dev/null | grep -q "post_x.py post"; then
    echo "X post scheduler already installed in crontab."
    crontab -l | grep "post_x.py post"
    exit 0
fi

# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
echo "✓ Installed X post scheduler (every Tuesday 9:00 AM):"
echo "  $CRON_LINE"
echo ""
echo "Verify with: crontab -l"
echo "Remove with: crontab -l | grep -v post_x.py | crontab -"
