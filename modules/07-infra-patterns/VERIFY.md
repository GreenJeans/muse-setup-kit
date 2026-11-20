# Verify — Module 07: Infra Patterns

## At install

- [ ] The backup layout is recorded in the workstream's home: what is
      imaged, locations, retention, stated exclusions, restore steps.
- [ ] Capacity math checks out: retention × image size fits the target
      storage with room to spare, and the image target is not the disk
      being protected.
- [ ] The verify pass runs and reports an integrity result per guest.
- [ ] **Test restores pass from every layer** — including the offsite
      layer, byte-compared — before any layer is called live.
- [ ] Alerts are wired, and the user has seen one routine-priority and
      one emergency-priority test alert.

## Deferred

- [ ] **Kill-a-service drill** (due: first week): a watched service is
      stopped; an alert arrives; on restart, a recovery note follows and
      no repeat alerts fire.
- [ ] **First scheduled verify** (due: first week): the unattended pass
      reports OK — or its failure is itself reported.
