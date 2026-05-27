from datetime import datetime, timezone

from fastapi import HTTPException


def validate_expiry(expiry: datetime):

    # Convert naive datetime to UTC-aware
    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)

    if expiry < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Cannot donate expired food",
        )


def verify_donation_owner(
    donation,
    current_user,
):
    if donation.donor_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized",
        )