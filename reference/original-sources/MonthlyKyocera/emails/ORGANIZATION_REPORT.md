# Email Organization Report

## Summary
- **Total Files**: 185 (100 .eml + 85 .msg)
- **Unique Serial Numbers**: 28 devices
- **Email Types**: Counter readings, Toner alerts, Undeliverable messages

## Preservation Strategy
✅ **All original files preserved in multiple locations:**
1. `emails/pending/` - Original working directory (185 files)
2. `emails/originals/` - Complete backup copy (185 files)
3. `emails/organized/` - Organized copies by serial and type

## Organization Structure

```
emails/
├── pending/          # Original files (PRESERVED)
├── originals/        # Backup copy (PRESERVED)
└── organized/        # Organized copies
    ├── by-serial/    # Grouped by device serial number
    │   ├── W7F3601552/  (14 files - Counter, Toner, duplicates)
    │   ├── W7F3701713/  (14 files)
    │   ├── W7F3601570/  (13 files)
    │   └── ... (28 serial folders total)
    ├── by-type/      # Grouped by email type
    │   ├── counter/  # Meter reading emails
    │   └── toner/    # Toner alert emails
    └── undeliverable/  # Failed delivery notifications

```

## Duplicate Handling Strategy

### Types of Duplicates Found:
1. **Same email in both formats**: .eml and .msg versions
   - Example: `W7F3601552.eml` and `W7F3601552.msg`
   - These are the same email in different formats

2. **Multiple readings over time**: Numbered versions (1), (2), (3), etc.
   - Example: `W7F3601552.eml`, `W7F3601552 (1).eml`, `W7F3601552 (2).eml`
   - These are different readings from different dates

3. **Different email types**: Counter vs Toner for same device
   - Counter readings: Device usage statistics
   - Toner alerts: Maintenance notifications

### Recommendation:
- Keep all duplicates as they represent different time periods
- Process numbered versions chronologically
- Use .eml format as primary (more portable)
- Keep .msg as backup (Outlook-specific features)

## Top Devices by Email Count
1. W7F3701713: 14 files
2. W7F3601552: 14 files
3. W7F3601570: 13 files
4. W794302146: 13 files
5. W7F3601563: 12 files
6. W7F3601555: 12 files
7. W7F3601615: 10 files
8. W792300234: 9 files
9. W7F3601564: 7 files
10. W7F3501393: 7 files

## Next Steps
1. Process emails to extract meter readings
2. Generate PDF/TXT reports per device
3. Archive processed emails
4. Create device-specific folders with date hierarchy