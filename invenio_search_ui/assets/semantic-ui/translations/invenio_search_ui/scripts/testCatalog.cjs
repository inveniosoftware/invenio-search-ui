// SPDX-FileCopyrightText: 2026 KTH Royal Institute of Technology.
// SPDX-License-Identifier: MIT

const assert = require("node:assert/strict");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { spawnSync } = require("node:child_process");
const test = require("node:test");
const i18next = require("i18next");
const { Parser } = require("i18next-scanner");
const { options } = require("../i18next-scanner.config.js");

const source = `msgid ""
msgstr ""
"Language: de\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\\n"

msgid "Reviewed"
msgstr "Geprüft"

#, python-format, fuzzy
msgid "Needs review"
msgstr "Ungeprüft"

msgid "item"
msgid_plural "items"
msgstr[0] "Ding"
msgstr[1] "Dinge"

msgid "Missing"
msgstr ""
`;

test("compile reviewed entries and v4 plurals; fall back for fuzzy entries", async () => {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), "i18n-catalog-"));
  try {
    const messages = path.join(directory, "messages", "de");
    fs.mkdirSync(messages, { recursive: true });
    fs.writeFileSync(path.join(messages, "messages.po"), source);
    const result = spawnSync(
      process.execPath,
      [path.join(__dirname, "compileCatalog.js")],
      {
        cwd: directory,
        encoding: "utf8",
      }
    );
    assert.equal(result.status, 0, result.stderr);
    const translations = JSON.parse(
      fs.readFileSync(path.join(messages, "translations.json"), "utf8")
    );
    assert.equal(translations.Reviewed, "Geprüft");
    assert.equal(translations["Needs review"], undefined);
    assert.equal(translations.Missing, undefined);
    assert.equal(translations.item_one, "Ding");
    assert.equal(translations.item_other, "Dinge");
    const runtime = i18next.createInstance();
    await runtime.init({
      lng: "de",
      fallbackLng: "en",
      debug: false,
      keySeparator: false,
      nsSeparator: false,
      resources: {
        de: { translation: translations },
        en: {
          translation: { "Needs review": "Needs review", "Missing": "Missing" },
        },
      },
    });
    assert.equal(runtime.t("Reviewed"), "Geprüft");
    assert.equal(runtime.t("Needs review"), "Needs review");
    assert.equal(runtime.t("Missing"), "Missing");
    assert.equal(runtime.t("item", { count: 1 }), "Ding");
    assert.equal(runtime.t("item", { count: 2 }), "Dinge");
  } finally {
    fs.rmSync(directory, { recursive: true, force: true });
  }
});

test("extract complete source messages", () => {
  const sourceRoot = path.resolve(__dirname, "../../../js");
  const cases = [
    [
      "invenio_search_ui/components/InvenioSearchPagination.js",
      ["<pageSize/> results per page", "<bold>{{count}}</bold> results found"],
    ],
    ["invenio_search_ui/components/Results.js", ["<resultCount/> result(s) found"]],
  ];
  for (const [filename, messages] of cases) {
    const parser = new Parser({ ...options, debug: false });
    const source = fs.readFileSync(path.join(sourceRoot, filename), "utf8");
    parser.parseFuncFromString(source);
    parser.parseTransFromString(source);
    const extracted = parser.get().en.translations;
    for (const message of messages) {
      assert.ok(
        Object.hasOwn(extracted, message) || Object.hasOwn(extracted, `${message}_one`),
        `${filename}: missing ${message}`
      );
    }
  }
});

test("keep the page-size control when translating its label", async () => {
  const React = require("react");
  const { TransWithoutContext } = require("react-i18next");
  const runtime = i18next.createInstance();
  const message = "<pageSize/> results per page";
  await runtime.init({
    lng: "sv",
    fallbackLng: "en",
    keySeparator: false,
    nsSeparator: false,
    resources: {
      sv: { translation: { [message]: "Resultat per sida: <pageSize/>" } },
    },
  });
  const PageSize = () => null;
  const onChange = () => {};
  const control = React.createElement(PageSize, { value: 25, onChange });
  const output = TransWithoutContext({
    i18n: runtime,
    defaults: message,
    components: { pageSize: control },
  });
  assert.equal(output[0], "Resultat per sida: ");
  const translatedControl = output.find(React.isValidElement);
  assert.equal(translatedControl.type, PageSize);
  assert.equal(translatedControl.props.value, 25);
  assert.equal(translatedControl.props.onChange, onChange);
});
