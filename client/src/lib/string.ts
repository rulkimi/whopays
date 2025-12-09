export const generateUsernameSuggestion = (watchedName: string, currentUsername: string) => {
  if (!watchedName || watchedName.trim().length === 0) return "";

  const parts = watchedName.trim().toLowerCase().split(/\s+/);
  const option1 = parts.join("_");
  let option2 = "";
  if (parts.length >= 2) {
    option2 = parts[0] + "_" + parts.slice(1).join("_");
  }
  let option3 = "";
  if (parts.length >= 2) {
    option3 = parts.slice(-2).join("_");
  }
  const rand = Math.floor(10000 + Math.random() * 90000);
  const options = [option1, option2, option3].filter(x => x);
  let suggestion = options.find(opt => opt !== currentUsername) || option1;
  suggestion += `_${rand}`;
  return suggestion;
}
