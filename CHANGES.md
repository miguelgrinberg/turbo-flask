# Turbo-Flask change log

**Release 0.8.5** - 2024-07-30

- Update hotwire turbo to version 8.0.5 ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/ec1e3f268214744030272314c1663be79fab4a4b))

**Release 0.8.4** - 2023-03-04

- Update turbo.js to 7.3.0 ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/a7944a6b10852555c2882be71a4b2e209d07a630))
- Document use of nginx as reverse proxy [#44](https://github.com/miguelgrinberg/turbo-flask/issues/44) ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/39407dd7a9bef74fc89f43616f516e27e3ed78fa))
- Remove deprecated `@before_first_request` decorator from "load" example ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/6a24b2d93ea1da0d1c17f104131dfd901c30a24d))

**Release 0.8.3** - 2022-10-27

- Switch CDN from skypack to jsdelivr [#42](https://github.com/miguelgrinberg/turbo-flask/issues/42) ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/0292e5831fb48cb32312ca5dec323fdc9c665375))

**Release 0.8.2** - 2022-10-17

- Upgrade to turbo.js 7.2.2 [#41](https://github.com/miguelgrinberg/turbo-flask/issues/41) ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/2c933ae229bcbfe1782202cd425d84595fa9387b)) (thanks **Oliver Wehrens**!)

**Release 0.8.1** - 2022-09-24

- Update turbo.js to 7.2.0 [#39](https://github.com/miguelgrinberg/turbo-flask/issues/39) ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/f083aba4f8fe4a190c4670b89b9113ccc2ff725f)) (thanks **Jan Peterka**!)
- Example of how to flash message from a turbo-stream ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/fc6fdc255d41dbe205009fda07440f3040040662))
- Readme files for all examples ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/51e42153740e64b1649cca949225322aad943129))
- Add python 3.10 to builds ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/461da5f0112ba9ff96c0745a23875855fb75b306))
- Upgrade build to pypy-3.9 ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/f6e2b09deba21e5d8f5c710ae9aaf0e43e634c0f))

**Release 0.8.0** - 2021-11-26

- Upgrade to turbo.js 7.1.0 [#20](https://github.com/miguelgrinberg/turbo-flask/issues/20) ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/7a55661c847e04838c791b571b06bfc8f67ada81)) (thanks **Jan Peterka**!)

**Release 0.7.0** - 2021-11-03

- Add after and before streams, and upgrade to turbo.js v7.0.1 [#18](https://github.com/miguelgrinberg/turbo-flask/issues/18) ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/f66fbe5637ad29c97a6e081d093e3a17067a7c42)) (thanks **Jan Peterka**!)
- Fix turbo stream close tag in todos example [#15](https://github.com/miguelgrinberg/turbo-flask/issues/15) ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/60c3568ecfebfe20031faee1f2e17de257d73746)) (thanks **John Jansen**!)

**Release 0.6.1** - 2021-09-17

- Upgrade to turbo.js v7-rc4 ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/5986e9c5ca55e8dac09f4840dc9aa658dd26dda1))
- Silence broken pipe errors from the WebSocket layer [#9](https://github.com/miguelgrinberg/turbo-flask/issues/9) ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/00d1102ad095ecfd675b02ab7d35d69ee2448445))
- More unit tests ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/1024af5285c2098f4284570caac64279a1aaa2a3))

**Release 0.6.0** - 2021-06-30

- Respect scheme of page when connecting via websocket [#8](https://github.com/miguelgrinberg/turbo-flask/issues/8) ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/554ceeabed57a50a8f60b4c1c19a31c543475c87))
- Better handling of the "to" argument in push() ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/ac9f18bd04c2812655831df4770ef74f61058a09))
- Handle unexpectedly closed WebSockets ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/d2b59e1022a48158da45fa65c9db223c9af1e4d7))
- Make load example work on Mac and Windows with fake load averages ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/02f8e8fe9edc43604d9fe1697f48c200ed5b665b))
- Added change log ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/3d238c1a299ce354abde7555a6266246317d57fe))
- Sphinx documentation ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/becf0e30b09fd95e2ea2be250fb38bae397db3d6))

**Release 0.5.0** - 2021-05-08

- Added `requested_frame()` method ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/71deb03d91b855f84cc153f29eaf50973045e050))
- Updated turbo.js to v7-beta5 ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/012948ab36fdd7ecf0714e270818dfe200d4d085))
- Stream pushing example ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/2777419fecec2cbe01ed2e4f5fcb5c23ed575429))
- Stream updates over WebSocket ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/7ef9c47dc1f1369751ea56200d6597f07226d5cf))

**Release 0.0.1** - 2021-01-31

- Initial release ([commit](https://github.com/miguelgrinberg/turbo-flask/commit/968bb3686dc19dbc4ab0b6c391ab964b7921a534))
