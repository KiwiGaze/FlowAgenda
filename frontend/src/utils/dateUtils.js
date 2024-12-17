// utils/dateUtils.js
export const isDateInRange = (date, days) => {
  const now = new Date();
  const past = new Date(now.setDate(now.getDate() - days));
  return new Date(date) >= past;
};