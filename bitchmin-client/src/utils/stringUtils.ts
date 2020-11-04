const titleCase = (str: string) => str
    .split(' ')
    .map(
        ([firstChar, ...rest]) => firstChar.toUpperCase() + rest.join('').toLowerCase(),
    )
    .join(' ');

export { titleCase };
