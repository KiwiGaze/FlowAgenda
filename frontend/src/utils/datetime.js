// src/utils/datetime.js

/**
 * Utility functions for handling date and time conversions between
 * frontend components and Django backend
 */

/**
 * Convert ISO datetime string from backend to separate date and time
 * @param {string} isoString - ISO datetime string from backend
 * @returns {{date: string, time: string}} Separated date and time strings
 */
export function parseBackendDateTime(isoString) {
  if (!isoString) return { date: '', time: '' };
  
  try {
    const date = new Date(isoString);
    if (isNaN(date.getTime())) return { date: '', time: '' };
    
    return {
      date: formatDateToISO(date), // Now returns YYYY-MM-DD
      time: formatTimeForDisplay(date) // Returns HH:MM AM/PM
    };
  } catch (error) {
    console.error('Error parsing backend datetime:', error);
    return { date: '', time: '' };
  }
}

/**
 * Format Date object to ISO date string (YYYY-MM-DD)
 * @param {Date} date - Date object to format
 * @returns {string} ISO formatted date string
 */
export function formatDateToISO(date) {
  return date.toISOString().split('T')[0];
}

/**
 * Format Date object to 12-hour time string (HH:MM AM/PM)
 * @param {Date} date - Date object to format
 * @returns {string} Formatted time string
 */
export function formatTimeForDisplay(date) {
  let hours = date.getHours();
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const period = hours >= 12 ? 'PM' : 'AM';
  
  // Convert to 12-hour format
  if (hours > 12) hours -= 12;
  if (hours === 0) hours = 12;
  
  return `${String(hours).padStart(2, '0')}:${minutes}${period}`;
}

/**
 * Create ISO datetime string for backend from date and time components
 * @param {string} dateStr - Date in YYYY-MM-DD format
 * @param {string} timeStr - Time in HH:MM AM/PM format
 * @returns {string} ISO datetime string for backend
 */
export function createBackendDateTime(dateStr, timeStr) {
  if (!dateStr || !timeStr) return null;
  
  try {
    // Parse date from ISO format
    const [year, month, day] = dateStr.split('-').map(Number);
    
    // Convert time to 24-hour format
    const time24 = convertTo24Hour(timeStr);
    const [hours, minutes] = time24.split(':').map(Number);
    
    // Create date object and return ISO string
    const date = new Date(Date.UTC(year, month - 1, day, hours, minutes));
    
    if (isNaN(date.getTime())) return null;
    
    return date.toISOString();
  } catch (error) {
    console.error('Error creating backend datetime:', error);
    return null;
  }
}

/**
 * Calculate default end datetime (1 hour from start)
 * @param {string} startDate - Start date in YYYY-MM-DD format
 * @param {string} startTime - Start time in HH:MM AM/PM format
 * @returns {{date: string, time: string}} Default end date/time
 */
export function calculateDefaultEndDateTime(startDate, startTime) {
  if (!startDate || !startTime) return { date: '', time: '' };
  
  try {
    const startDateTime = new Date(createBackendDateTime(startDate, startTime));
    if (isNaN(startDateTime.getTime())) return { date: '', time: '' };
    
    const endDateTime = new Date(startDateTime.getTime() + 60 * 60 * 1000);
    
    return {
      date: formatDateToISO(endDateTime),
      time: formatTimeForDisplay(endDateTime)
    };
  } catch (error) {
    console.error('Error calculating default end datetime:', error);
    return { date: '', time: '' };
  }
}

/**
 * Validate if end datetime is after start datetime
 * @param {string} startDate - Start date in YYYY-MM-DD format
 * @param {string} startTime - Start time in HH:MM AM/PM format
 * @param {string} endDate - End date in YYYY-MM-DD format
 * @param {string} endTime - End time in HH:MM AM/PM format
 * @returns {boolean} True if end is after start
 */
export function isValidDateTimeRange(startDate, startTime, endDate, endTime) {
  if (!endDate || !endTime) return true;
  if (!startDate || !startTime) return false;
  
  try {
    const startISO = createBackendDateTime(startDate, startTime);
    const endISO = createBackendDateTime(endDate, endTime);
    
    if (!startISO || !endISO) return false;
    
    const start = new Date(startISO);
    const end = new Date(endISO);
    
    return end > start;
  } catch (error) {
    console.error('Error validating datetime range:', error);
    return false;
  }
}

/**
 * Parse ISO date string to date display format
 * @param {string} isoDate - Date in ISO format (YYYY-MM-DD)
 * @returns {string} Date in display format (YYYY-MM-DD)
 */
export function parseDateForDisplay(isoDate) {
  if (!isoDate) return '';
  
  try {
    const date = new Date(isoDate);
    if (isNaN(date.getTime())) return '';
    return formatDateToISO(date);
  } catch (error) {
    console.error('Error parsing date for display:', error);
    return '';
  }
}

/**
 * Format a full ISO datetime string for display
 * @param {string} isoString - Full ISO datetime string
 * @returns {string} Formatted datetime for display
 */
export function formatDateTimeForDisplay(isoString) {
  if (!isoString) return '';
  
  try {
    const date = new Date(isoString);
    if (isNaN(date.getTime())) return '';
    
    return `${formatDateToISO(date)} ${formatTimeForDisplay(date)}`;
  } catch (error) {
    console.error('Error formatting datetime for display:', error);
    return '';
  }
}

/**
 * Convert 24-hour time string to 12-hour format with AM/PM
 * @param {string} time24h - Time in 24-hour format (HH:mm)
 * @returns {string} Time in 12-hour format (HH:MM AM/PM)
 */
export function convertTo12Hour(time24h) {
  if (!time24h) return '';
  
  try {
    const [hours24, minutes] = time24h.split(':').map(Number);
    
    if (isNaN(hours24) || isNaN(minutes)) return '';
    
    let period = hours24 >= 12 ? 'PM' : 'AM';
    let hours12 = hours24 % 12;
    if (hours12 === 0) hours12 = 12;
    
    return `${String(hours12).padStart(2, '0')}:${String(minutes).padStart(2, '0')}${period}`;
  } catch (error) {
    console.error('Error converting time to 12-hour format:', error);
    return '';
  }
}

/**
 * Convert 12-hour time string to 24-hour format
 * @param {string} time12h - Time in 12-hour format (HH:MM AM/PM)
 * @returns {string} Time in 24-hour format (HH:mm)
 */
export function convertTo24Hour(time12h) {
  if (!time12h) return '';
  
  try {
    const match = time12h.match(/^(\d{1,2}):(\d{2})(AM|PM)$/i);
    if (!match) return '';
    
    let [_, hours, minutes, period] = match;
    hours = parseInt(hours);
    
    if (period.toUpperCase() === 'PM' && hours !== 12) {
      hours += 12;
    } else if (period.toUpperCase() === 'AM' && hours === 12) {
      hours = 0;
    }
    
    return `${String(hours).padStart(2, '0')}:${minutes}`;
  } catch (error) {
    console.error('Error converting time to 24-hour format:', error);
    return '';
  }
}

/**
 * Parse backend datetime to get time in 12-hour format
 * @param {string} isoString - ISO datetime string from backend
 * @returns {string} Time in 12-hour format (HH:MM AM/PM)
 */
export function parseBackendTime(isoString) {
  if (!isoString) return '';
  
  try {
    const date = new Date(isoString);
    if (isNaN(date.getTime())) return '';
    
    const hours24 = date.getHours();
    const minutes = date.getMinutes();
    
    return convertTo12Hour(`${hours24}:${minutes}`);
  } catch (error) {
    console.error('Error parsing backend time:', error);
    return '';
  }
}