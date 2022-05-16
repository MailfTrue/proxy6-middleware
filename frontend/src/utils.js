let regionNames = new Intl.DisplayNames(['ru'], {type: 'region'});


export function countryName(country) {
    return regionNames.of(country.toUpperCase())
}


export function countryPretty(country) {
    return `${countryEmoji(country)} ${countryName(country)}`
}


export function countryEmoji(country) {
    country = country.toUpperCase()
    const offset = 127397;
    const A = 65;
    const Z = 90;

    const f = country.codePointAt(0);
    const s = country.codePointAt(1);

    if (
        country.length !== 2
        || f > Z || f < A
        || s > Z || s < A
    )
        throw new Error('Not an alpha2 country code');

    return String.fromCodePoint(f + offset)
        +String.fromCodePoint(s + offset);
}