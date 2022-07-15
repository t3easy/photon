%global security_hardening none

%ifarch x86_64
%define arch x86_64
%define archdir x86

# Set this flag to 0 to build without canister
%global fips 1

# If kat_build is enabled, canister is not used.
%if 0%{?kat_build}
%global fips 0
%endif

%endif

Summary:        Kernel
Name:           linux-rt
Version:        5.10.118
Release:        10%{?kat_build:.kat}%{?dist}
License:        GPLv2
URL:            http://www.kernel.org/
Group:          System Environment/Kernel
Vendor:         VMware, Inc.
Distribution:   Photon

# Keep rt_version matched up with localversion.patch
%define rt_version rt67
%define uname_r %{version}-%{rt_version}-%{release}-rt
%define _modulesdir /lib/modules/%{uname_r}

Source0:        http://www.kernel.org/pub/linux/kernel/v5.x/linux-%{version}.tar.xz
%define sha512 linux=5ce0746c3b519abe9e20d1c80264a6a8e49bc18907cc0712fd0520f8e74806028a1b3929da636d6ab88b195895f1873122122b1506b7047c37ba30ed22b357f1
Source1:    config-rt
Source2:    initramfs.trigger
Source4:    pre-preun-postun-tasks.inc
Source5:    check_for_config_applicability.inc

%define i40e_version 2.15.9
Source6:    https://sourceforge.net/projects/e1000/files/i40e%20stable/%{i40e_version}/i40e-%{i40e_version}.tar.gz
%define sha512 i40e=891723116fca72c51851d7edab0add28c2a0b4c4768a7646794c8b3bc4d44a1786115e67f05cfa5bb3bc484a4e07145fc4640a621f3bc755cc07257b1b531dd5

%define iavf_version 4.2.7
Source7:       https://sourceforge.net/projects/e1000/files/iavf%20stable/%{iavf_version}/iavf-%{iavf_version}.tar.gz
%define sha512 iavf=1f491d9ab76444db1d5f0edbd9477eb3b15fa75f73785715ff8af31288b0490c01b54cc50b6bac3fc36d9caf25bae94fb4ef4a7e73d4360c7031ece32d725e70

%define ice_version 1.6.4
Source8:       https://sourceforge.net/projects/e1000/files/ice%20stable/%{ice_version}/ice-%{ice_version}.tar.gz
%define sha512 ice=e88be3b416184d5c157aecda79b2580403b67c68286221ae154a92fa1d46cacd23aa55365994fa53f266d6df4ca2046cc2fcb35620345fd23e80b90a45ec173c

%if 0%{?fips}
Source9:        check_fips_canister_struct_compatibility.inc

%define fips_canister_version 4.0.1-5.10.21-3-secure
Source16:       fips-canister-%{fips_canister_version}.tar.bz2
%define sha512 fips-canister=1d3b88088a23f7d6e21d14b1e1d29496ea9e38c750d8a01df29e1343034f74b0f3801d1f72c51a3d27e9c51113c808e6a7aa035cb66c5c9b184ef8c4ed06f42a
Source18:        fips_canister-kallsyms
%endif

Source17:        modify_kernel_configs.inc
# common
Patch0: net-Double-tcp_mem-limits.patch
Patch1: SUNRPC-Do-not-reuse-srcport-for-TIME_WAIT-socket.patch
Patch2: SUNRPC-xs_bind-uses-ip_local_reserved_ports.patch
Patch3: 9p-transport-for-9p.patch
Patch4: 9p-trans_fd-extend-port-variable-to-u32.patch
Patch5: vsock-delay-detach-of-QP-with-outgoing-data-59.patch
# RDRAND-based RNG driver to enhance the kernel's entropy pool:
Patch6: hwrng-rdrand-Add-RNG-driver-based-on-x86-rdrand-inst.patch
Patch7: 0001-cgroup-v1-cgroup_stat-support.patch

# ttyXRUSB support
Patch10: usb-acm-exclude-exar-usb-serial-ports-nxt.patch

Patch12: fork-add-sysctl-to-disallow-unprivileged-CLONE_NEWUSER-by.patch
# Out-of-tree patches from AppArmor:
Patch13: apparmor-patch-to-provide-compatibility-with-v2.x-ne.patch
Patch14: apparmor-af_unix-mediation.patch

#vmxnet3
Patch20: 0001-vmxnet3-Remove-buf_info-from-device-accessible-struc.patch

# VMW:
Patch55: x86-vmware-Use-Efficient-and-Correct-ALTERNATIVEs-fo-510.patch
Patch56: x86-vmware-Log-kmsg-dump-on-panic-510.patch
Patch57: 0001-x86-vmware-avoid-TSC-recalibration.patch

# CVE:
Patch100: apparmor-fix-use-after-free-in-sk_peer_label.patch
# Fix for CVE-2019-12379
Patch101: consolemap-Fix-a-memory-leaking-bug-in-drivers-tty-v.patch

# Next 2 patches are about to be merged into stable
Patch102: 0001-mm-fix-panic-in-__alloc_pages.patch

# Fix for CVE-2021-4204
Patch103: 0002-bpf-Disallow-unprivileged-bpf-by-default.patch
# Fix for CVE-2022-21499
Patch104: 0001-debug-Lock-down-kgdb.patch
# Fix for CVE-2022-1966
Patch105: 0001-netfilter_nf_tables_disallow_non-stateful_expression_in_sets.patch
# Fix for CVE-2022-1972
Patch106: 0001-netfilter_nf_tables_sanitize_nft_set_desc_concat_parse.patch
# Fix for CVE-2022-21505
Patch107: 0001-ima-Verify-ima-appraisal-is-set-to-enforce.patch

# Allow PCI resets to be disabled from vfio_pci module
Patch120: 0001-drivers-vfio-pci-Add-kernel-parameter-to-allow-disab.patch
# Add PCI quirk to allow multiple devices under the same virtual PCI bridge
# to be put into separate IOMMU groups on ESXi.
Patch121: 0001-Add-PCI-quirk-for-VMware-PCIe-Root-Port.patch

# Real-Time kernel (PREEMPT_RT patches)
# Source: http://cdn.kernel.org/pub/linux/kernel/projects/rt/5.10/
Patch301: 0001-z3fold-remove-preempt-disabled-sections-for-RT.patch
Patch302: 0002-stop_machine-Add-function-and-caller-debug-info.patch
Patch303: 0003-sched-Fix-balance_callback.patch
Patch304: 0004-sched-hotplug-Ensure-only-per-cpu-kthreads-run-durin.patch
Patch305: 0005-sched-core-Wait-for-tasks-being-pushed-away-on-hotpl.patch
Patch306: 0006-workqueue-Manually-break-affinity-on-hotplug.patch
Patch307: 0007-sched-hotplug-Consolidate-task-migration-on-CPU-unpl.patch
Patch308: 0008-sched-Fix-hotplug-vs-CPU-bandwidth-control.patch
Patch309: 0009-sched-Massage-set_cpus_allowed.patch
Patch310: 0010-sched-Add-migrate_disable.patch
Patch311: 0011-sched-Fix-migrate_disable-vs-set_cpus_allowed_ptr.patch
Patch312: 0012-sched-core-Make-migrate-disable-and-CPU-hotplug-coop.patch
Patch313: 0013-sched-rt-Use-cpumask_any-_distribute.patch
Patch314: 0014-sched-rt-Use-the-full-cpumask-for-balancing.patch
Patch315: 0015-sched-lockdep-Annotate-pi_lock-recursion.patch
Patch316: 0016-sched-Fix-migrate_disable-vs-rt-dl-balancing.patch
Patch317: 0017-sched-proc-Print-accurate-cpumask-vs-migrate_disable.patch
Patch318: 0018-sched-Add-migrate_disable-tracepoints.patch
Patch319: 0019-sched-Deny-self-issued-__set_cpus_allowed_ptr-when-m.patch
Patch320: 0020-sched-Comment-affine_move_task.patch
Patch321: 0021-sched-Unlock-the-rq-in-affine_move_task-error-path.patch
Patch322: 0022-sched-Fix-migration_cpu_stop-WARN.patch
Patch323: 0023-sched-core-Add-missing-completion-for-affine_move_ta.patch
Patch324: 0024-mm-highmem-Un-EXPORT-__kmap_atomic_idx.patch
Patch325: 0025-highmem-Remove-unused-functions.patch
Patch326: 0026-fs-Remove-asm-kmap_types.h-includes.patch
Patch327: 0027-sh-highmem-Remove-all-traces-of-unused-cruft.patch
Patch328: 0028-asm-generic-Provide-kmap_size.h.patch
Patch329: 0029-highmem-Provide-generic-variant-of-kmap_atomic.patch
Patch330: 0030-highmem-Make-DEBUG_HIGHMEM-functional.patch
Patch331: 0031-x86-mm-highmem-Use-generic-kmap-atomic-implementatio.patch
Patch332: 0032-arc-mm-highmem-Use-generic-kmap-atomic-implementatio.patch
Patch333: 0033-ARM-highmem-Switch-to-generic-kmap-atomic.patch
Patch334: 0034-csky-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch335: 0035-microblaze-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch336: 0036-mips-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch337: 0037-nds32-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch338: 0038-powerpc-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch339: 0039-sparc-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch340: 0040-xtensa-mm-highmem-Switch-to-generic-kmap-atomic.patch
Patch341: 0041-highmem-Get-rid-of-kmap_types.h.patch
Patch342: 0042-mm-highmem-Remove-the-old-kmap_atomic-cruft.patch
Patch343: 0043-io-mapping-Cleanup-atomic-iomap.patch
Patch344: 0044-Documentation-io-mapping-Remove-outdated-blurb.patch
Patch345: 0045-highmem-High-implementation-details-and-document-API.patch
Patch346: 0046-sched-Make-migrate_disable-enable-independent-of-RT.patch
Patch347: 0047-sched-highmem-Store-local-kmaps-in-task-struct.patch
Patch348: 0048-mm-highmem-Provide-kmap_local.patch
Patch349: 0049-io-mapping-Provide-iomap_local-variant.patch
Patch350: 0050-x86-crashdump-32-Simplify-copy_oldmem_page.patch
Patch351: 0051-mips-crashdump-Simplify-copy_oldmem_page.patch
Patch352: 0052-ARM-mm-Replace-kmap_atomic_pfn.patch
Patch353: 0053-highmem-Remove-kmap_atomic_pfn.patch
Patch354: 0054-drm-ttm-Replace-kmap_atomic-usage.patch
Patch355: 0055-drm-vmgfx-Replace-kmap_atomic.patch
Patch356: 0056-highmem-Remove-kmap_atomic_prot.patch
Patch357: 0057-drm-qxl-Replace-io_mapping_map_atomic_wc.patch
Patch358: 0058-drm-nouveau-device-Replace-io_mapping_map_atomic_wc.patch
Patch359: 0059-drm-i915-Replace-io_mapping_map_atomic_wc.patch
Patch360: 0060-io-mapping-Remove-io_mapping_map_atomic_wc.patch
Patch361: 0061-mm-highmem-Take-kmap_high_get-properly-into-account.patch
Patch362: 0062-highmem-Don-t-disable-preemption-on-RT-in-kmap_atomi.patch
Patch363: 0063-blk-mq-Don-t-complete-on-a-remote-CPU-in-force-threa.patch
Patch364: 0064-blk-mq-Always-complete-remote-completions-requests-i.patch
Patch365: 0065-blk-mq-Use-llist_head-for-blk_cpu_done.patch
Patch366: 0066-lib-test_lockup-Minimum-fix-to-get-it-compiled-on-PR.patch
Patch367: 0067-timers-Don-t-block-on-expiry_lock-for-TIMER_IRQSAFE.patch
Patch368: 0068-kthread-Move-prio-affinite-change-into-the-newly-cre.patch
Patch369: 0069-genirq-Move-prio-assignment-into-the-newly-created-t.patch
Patch370: 0070-notifier-Make-atomic_notifiers-use-raw_spinlock.patch
Patch371: 0071-rcu-Make-RCU_BOOST-default-on-CONFIG_PREEMPT_RT.patch
Patch372: 0072-rcu-Unconditionally-use-rcuc-threads-on-PREEMPT_RT.patch
Patch373: 0073-rcu-Enable-rcu_normal_after_boot-unconditionally-for.patch
Patch374: 0074-doc-Update-RCU-s-requirements-page-about-the-PREEMPT.patch
Patch375: 0075-doc-Use-CONFIG_PREEMPTION.patch
Patch376: 0076-tracing-Merge-irqflags-preempt-counter.patch
Patch377: 0077-tracing-Inline-tracing_gen_ctx_flags.patch
Patch378: 0078-tracing-Use-in_serving_softirq-to-deduct-softirq-sta.patch
Patch379: 0079-tracing-Remove-NULL-check-from-current-in-tracing_ge.patch
Patch380: 0080-printk-inline-log_output-log_store-in-vprintk_store.patch
Patch381: 0081-printk-remove-logbuf_lock-writer-protection-of-ringb.patch
Patch382: 0082-printk-limit-second-loop-of-syslog_print_all.patch
Patch383: 0083-printk-kmsg_dump-remove-unused-fields.patch
Patch384: 0084-printk-refactor-kmsg_dump_get_buffer.patch
Patch385: 0085-printk-consolidate-kmsg_dump_get_buffer-syslog_print.patch
Patch386: 0086-printk-introduce-CONSOLE_LOG_MAX-for-improved-multi-.patch
Patch387: 0087-printk-use-seqcount_latch-for-clear_seq.patch
Patch388: 0088-printk-use-atomic64_t-for-devkmsg_user.seq.patch
Patch389: 0089-printk-add-syslog_lock.patch
Patch390: 0090-printk-introduce-a-kmsg_dump-iterator.patch
Patch391: 0091-um-synchronize-kmsg_dumper.patch
Patch392: 0092-printk-remove-logbuf_lock.patch
Patch393: 0093-printk-kmsg_dump-remove-_nolock-variants.patch
Patch394: 0094-printk-kmsg_dump-use-kmsg_dump_rewind.patch
Patch395: 0095-printk-console-remove-unnecessary-safe-buffer-usage.patch
Patch396: 0096-printk-track-limit-recursion.patch
Patch397: 0097-printk-remove-safe-buffers.patch
Patch398: 0098-printk-convert-syslog_lock-to-spin_lock.patch
Patch399: 0099-console-add-write_atomic-interface.patch
Patch400: 0100-serial-8250-implement-write_atomic.patch
Patch401: 0101-printk-relocate-printk_delay-and-vprintk_default.patch
Patch402: 0102-printk-combine-boot_delay_msec-into-printk_delay.patch
Patch403: 0103-printk-change-console_seq-to-atomic64_t.patch
Patch404: 0104-printk-introduce-kernel-sync-mode.patch
Patch405: 0105-printk-move-console-printing-to-kthreads.patch
Patch406: 0106-printk-remove-deferred-printing.patch
Patch407: 0107-printk-add-console-handover.patch
Patch408: 0108-printk-add-pr_flush.patch
Patch409: 0109-cgroup-use-irqsave-in-cgroup_rstat_flush_locked.patch
Patch410: 0110-mm-workingset-replace-IRQ-off-check-with-a-lockdep-a.patch
Patch411: 0111-tpm-remove-tpm_dev_wq_lock.patch
Patch412: 0112-shmem-Use-raw_spinlock_t-for-stat_lock.patch
Patch413: 0113-net-Move-lockdep-where-it-belongs.patch
Patch414: 0114-parisc-Remove-bogus-__IRQ_STAT-macro.patch
Patch415: 0115-sh-Get-rid-of-nmi_count.patch
Patch416: 0116-irqstat-Get-rid-of-nmi_count-and-__IRQ_STAT.patch
Patch417: 0117-um-irqstat-Get-rid-of-the-duplicated-declarations.patch
Patch418: 0118-ARM-irqstat-Get-rid-of-duplicated-declaration.patch
Patch419: 0119-arm64-irqstat-Get-rid-of-duplicated-declaration.patch
Patch420: 0120-asm-generic-irqstat-Add-optional-__nmi_count-member.patch
Patch421: 0121-sh-irqstat-Use-the-generic-irq_cpustat_t.patch
Patch422: 0122-irqstat-Move-declaration-into-asm-generic-hardirq.h.patch
Patch423: 0123-preempt-Cleanup-the-macro-maze-a-bit.patch
Patch424: 0124-softirq-Move-related-code-into-one-section.patch
Patch425: 0125-sh-irq-Add-missing-closing-parentheses-in-arch_show_.patch
Patch426: 0126-sched-cputime-Remove-symbol-exports-from-IRQ-time-ac.patch
Patch427: 0127-s390-vtime-Use-the-generic-IRQ-entry-accounting.patch
Patch428: 0128-sched-vtime-Consolidate-IRQ-time-accounting.patch
Patch429: 0129-irqtime-Move-irqtime-entry-accounting-after-irq-offs.patch
Patch430: 0130-irq-Call-tick_irq_enter-inside-HARDIRQ_OFFSET.patch
Patch431: 0131-smp-Wake-ksoftirqd-on-PREEMPT_RT-instead-do_softirq.patch
Patch432: 0132-net-arcnet-Fix-RESET-flag-handling.patch
Patch433: 0133-tasklets-Replace-barrier-with-cpu_relax-in-tasklet_u.patch
Patch434: 0134-tasklets-Use-static-inlines-for-stub-implementations.patch
Patch435: 0135-tasklets-Provide-tasklet_disable_in_atomic.patch
Patch436: 0136-tasklets-Use-spin-wait-in-tasklet_disable-temporaril.patch
Patch437: 0137-tasklets-Replace-spin-wait-in-tasklet_unlock_wait.patch
Patch438: 0138-tasklets-Replace-spin-wait-in-tasklet_kill.patch
Patch439: 0139-tasklets-Prevent-tasklet_unlock_spin_wait-deadlock-o.patch
Patch440: 0140-net-jme-Replace-link-change-tasklet-with-work.patch
Patch441: 0141-net-sundance-Use-tasklet_disable_in_atomic.patch
Patch442: 0142-ath9k-Use-tasklet_disable_in_atomic.patch
Patch443: 0143-atm-eni-Use-tasklet_disable_in_atomic-in-the-send-ca.patch
Patch444: 0144-PCI-hv-Use-tasklet_disable_in_atomic.patch
Patch445: 0145-firewire-ohci-Use-tasklet_disable_in_atomic-where-re.patch
Patch446: 0146-tasklets-Switch-tasklet_disable-to-the-sleep-wait-va.patch
Patch447: 0147-softirq-Add-RT-specific-softirq-accounting.patch
Patch448: 0148-irqtime-Make-accounting-correct-on-RT.patch
Patch449: 0149-softirq-Move-various-protections-into-inline-helpers.patch
Patch450: 0150-softirq-Make-softirq-control-and-processing-RT-aware.patch
Patch451: 0151-tick-sched-Prevent-false-positive-softirq-pending-wa.patch
Patch452: 0152-rcu-Prevent-false-positive-softirq-warning-on-RT.patch
Patch453: 0153-chelsio-cxgb-Replace-the-workqueue-with-threaded-int.patch
Patch454: 0154-chelsio-cxgb-Disable-the-card-on-error-in-threaded-i.patch
Patch455: 0155-x86-fpu-Simplify-fpregs_-un-lock.patch
Patch456: 0156-x86-fpu-Make-kernel-FPU-protection-RT-friendly.patch
Patch457: 0157-locking-rtmutex-Remove-cruft.patch
Patch458: 0158-locking-rtmutex-Remove-output-from-deadlock-detector.patch
Patch459: 0159-locking-rtmutex-Move-rt_mutex_init-outside-of-CONFIG.patch
Patch460: 0160-locking-rtmutex-Remove-rt_mutex_timed_lock.patch
Patch461: 0161-locking-rtmutex-Handle-the-various-new-futex-race-co.patch
Patch462: 0162-futex-Fix-bug-on-when-a-requeued-RT-task-times-out.patch
Patch463: 0163-locking-rtmutex-Make-lock_killable-work.patch
Patch464: 0164-locking-spinlock-Split-the-lock-types-header.patch
Patch465: 0165-locking-rtmutex-Avoid-include-hell.patch
Patch466: 0166-lockdep-Reduce-header-files-in-debug_locks.h.patch
Patch467: 0167-locking-split-out-the-rbtree-definition.patch
Patch468: 0168-locking-rtmutex-Provide-rt_mutex_slowlock_locked.patch
Patch469: 0169-locking-rtmutex-export-lockdep-less-version-of-rt_mu.patch
Patch470: 0170-sched-Add-saved_state-for-tasks-blocked-on-sleeping-.patch
Patch471: 0171-locking-rtmutex-add-sleeping-lock-implementation.patch
Patch472: 0172-locking-rtmutex-Allow-rt_mutex_trylock-on-PREEMPT_RT.patch
Patch473: 0173-locking-rtmutex-add-mutex-implementation-based-on-rt.patch
Patch474: 0174-locking-rtmutex-add-rwsem-implementation-based-on-rt.patch
Patch475: 0175-locking-rtmutex-add-rwlock-implementation-based-on-r.patch
Patch476: 0176-locking-rtmutex-wire-up-RT-s-locking.patch
Patch477: 0177-locking-rtmutex-add-ww_mutex-addon-for-mutex-rt.patch
Patch478: 0178-locking-rtmutex-Use-custom-scheduling-function-for-s.patch
Patch479: 0179-signal-Revert-ptrace-preempt-magic.patch
Patch480: 0180-preempt-Provide-preempt_-_-no-rt-variants.patch
Patch481: 0181-mm-vmstat-Protect-per-cpu-variables-with-preempt-dis.patch
Patch482: 0182-mm-memcontrol-Disable-preemption-in-__mod_memcg_lruv.patch
Patch483: 0183-xfrm-Use-sequence-counter-with-associated-spinlock.patch
Patch484: 0184-u64_stats-Disable-preemption-on-32bit-UP-SMP-with-RT.patch
Patch485: 0185-fs-dcache-use-swait_queue-instead-of-waitqueue.patch
Patch486: 0186-fs-dcache-disable-preemption-on-i_dir_seq-s-write-si.patch
Patch487: 0187-net-Qdisc-use-a-seqlock-instead-seqcount.patch
Patch488: 0188-net-Properly-annotate-the-try-lock-for-the-seqlock.patch
Patch489: 0189-kconfig-Disable-config-options-which-are-not-RT-comp.patch
Patch490: 0190-mm-Allow-only-SLUB-on-RT.patch
Patch491: 0191-sched-Disable-CONFIG_RT_GROUP_SCHED-on-RT.patch
Patch492: 0192-net-core-disable-NET_RX_BUSY_POLL-on-RT.patch
Patch493: 0193-efi-Disable-runtime-services-on-RT.patch
Patch494: 0194-efi-Allow-efi-runtime.patch
Patch495: 0195-rt-Add-local-irq-locks.patch
Patch496: 0196-signal-x86-Delay-calling-signals-in-atomic.patch
Patch497: 0197-Split-IRQ-off-and-zone-lock-while-freeing-pages-from.patch
Patch498: 0198-Split-IRQ-off-and-zone-lock-while-freeing-pages-from.patch
Patch499: 0199-mm-SLxB-change-list_lock-to-raw_spinlock_t.patch
Patch500: 0200-mm-SLUB-delay-giving-back-empty-slubs-to-IRQ-enabled.patch
Patch501: 0201-mm-slub-Always-flush-the-delayed-empty-slubs-in-flus.patch
Patch502: 0202-mm-slub-Don-t-resize-the-location-tracking-cache-on-.patch
Patch503: 0203-mm-page_alloc-Use-migrate_disable-in-drain_local_pag.patch
Patch504: 0204-mm-page_alloc-rt-friendly-per-cpu-pages.patch
Patch505: 0205-mm-slub-Make-object_map_lock-a-raw_spinlock_t.patch
Patch506: 0206-slub-Enable-irqs-for-__GFP_WAIT.patch
Patch507: 0207-slub-Disable-SLUB_CPU_PARTIAL.patch
Patch508: 0208-mm-memcontrol-Provide-a-local_lock-for-per-CPU-memcg.patch
Patch509: 0209-mm-memcontrol-Don-t-call-schedule_work_on-in-preempt.patch
Patch510: 0210-mm-memcontrol-Replace-local_irq_disable-with-local-l.patch
Patch511: 0211-mm-zsmalloc-copy-with-get_cpu_var-and-locking.patch
Patch512: 0212-mm-zswap-Use-local-lock-to-protect-per-CPU-data.patch
Patch513: 0213-x86-kvm-Require-const-tsc-for-RT.patch
Patch514: 0214-wait.h-include-atomic.h.patch
Patch515: 0215-sched-Limit-the-number-of-task-migrations-per-batch.patch
Patch516: 0216-sched-Move-mmdrop-to-RCU-on-RT.patch
Patch517: 0217-kernel-sched-move-stack-kprobe-clean-up-to-__put_tas.patch
Patch518: 0218-sched-Do-not-account-rcu_preempt_depth-on-RT-in-migh.patch
Patch519: 0219-sched-Disable-TTWU_QUEUE-on-RT.patch
Patch520: 0220-softirq-Check-preemption-after-reenabling-interrupts.patch
Patch521: 0221-softirq-Disable-softirq-stacks-for-RT.patch
Patch522: 0222-net-core-use-local_bh_disable-in-netif_rx_ni.patch
Patch523: 0223-pid.h-include-atomic.h.patch
Patch524: 0224-ptrace-fix-ptrace-vs-tasklist_lock-race.patch
Patch525: 0225-ptrace-fix-ptrace_unfreeze_traced-race-with-rt-lock.patch
Patch526: 0226-kernel-sched-add-put-get-_cpu_light.patch
Patch527: 0227-trace-Add-migrate-disabled-counter-to-tracing-output.patch
Patch528: 0228-locking-don-t-check-for-__LINUX_SPINLOCK_TYPES_H-on-.patch
Patch529: 0229-locking-Make-spinlock_t-and-rwlock_t-a-RCU-section-o.patch
Patch530: 0230-mm-vmalloc-Another-preempt-disable-region-which-suck.patch
Patch531: 0231-block-mq-do-not-invoke-preempt_disable.patch
Patch532: 0232-md-raid5-Make-raid5_percpu-handling-RT-aware.patch
Patch533: 0233-scsi-fcoe-Make-RT-aware.patch
Patch534: 0234-sunrpc-Make-svc_xprt_do_enqueue-use-get_cpu_light.patch
Patch535: 0235-rt-Introduce-cpu_chill.patch
Patch536: 0236-fs-namespace-Use-cpu_chill-in-trylock-loops.patch
Patch537: 0237-debugobjects-Make-RT-aware.patch
Patch538: 0238-net-Use-skbufhead-with-raw-lock.patch
Patch539: 0239-net-Dequeue-in-dev_cpu_dead-without-the-lock.patch
Patch540: 0240-net-dev-always-take-qdisc-s-busylock-in-__dev_xmit_s.patch
Patch541: 0241-irqwork-push-most-work-into-softirq-context.patch
Patch542: 0242-x86-crypto-Reduce-preempt-disabled-regions.patch
Patch543: 0243-crypto-Reduce-preempt-disabled-regions-more-algos.patch
Patch544: 0244-crypto-limit-more-FPU-enabled-sections.patch
Patch545: 0245-crypto-cryptd-add-a-lock-instead-preempt_disable-loc.patch
Patch546: 0246-panic-skip-get_random_bytes-for-RT_FULL-in-init_oops.patch
Patch547: 0247-x86-stackprotector-Avoid-random-pool-on-rt.patch
Patch548: 0248-random-Make-it-work-on-rt.patch
Patch549: 0249-net-Remove-preemption-disabling-in-netif_rx.patch
Patch550: 0250-lockdep-Make-it-RT-aware.patch
Patch551: 0251-lockdep-selftest-Only-do-hardirq-context-test-for-ra.patch
Patch552: 0252-lockdep-selftest-fix-warnings-due-to-missing-PREEMPT.patch
Patch553: 0253-lockdep-disable-self-test.patch
Patch554: 0254-drm-radeon-i915-Use-preempt_disable-enable_rt-where-.patch
Patch555: 0255-drm-i915-Don-t-disable-interrupts-on-PREEMPT_RT-duri.patch
Patch556: 0256-drm-i915-disable-tracing-on-RT.patch
Patch557: 0257-drm-i915-skip-DRM_I915_LOW_LEVEL_TRACEPOINTS-with-NO.patch
Patch558: 0258-drm-i915-gt-Only-disable-interrupts-for-the-timeline.patch
Patch559: 0259-cpuset-Convert-callback_lock-to-raw_spinlock_t.patch
Patch560: 0260-x86-Allow-to-enable-RT.patch
Patch561: 0261-mm-scatterlist-Do-not-disable-irqs-on-RT.patch
Patch562: 0262-sched-Add-support-for-lazy-preemption.patch
Patch563: 0263-x86-entry-Use-should_resched-in-idtentry_exit_cond_r.patch
Patch564: 0264-x86-Support-for-lazy-preemption.patch
Patch565: 0265-arm-Add-support-for-lazy-preemption.patch
Patch566: 0266-powerpc-Add-support-for-lazy-preemption.patch
Patch567: 0267-arch-arm64-Add-lazy-preempt-support.patch
Patch568: 0268-jump-label-disable-if-stop_machine-is-used.patch
Patch569: 0269-leds-trigger-disable-CPU-trigger-on-RT.patch
Patch570: 0270-tty-serial-omap-Make-the-locking-RT-aware.patch
Patch571: 0271-tty-serial-pl011-Make-the-locking-work-on-RT.patch
Patch572: 0272-ARM-enable-irq-in-translation-section-permission-fau.patch
Patch573: 0273-genirq-update-irq_set_irqchip_state-documentation.patch
Patch574: 0274-KVM-arm-arm64-downgrade-preempt_disable-d-region-to-.patch
Patch575: 0275-arm64-fpsimd-Delay-freeing-memory-in-fpsimd_flush_th.patch
Patch576: 0276-x86-Enable-RT-also-on-32bit.patch
Patch577: 0277-ARM-Allow-to-enable-RT.patch
Patch578: 0278-ARM64-Allow-to-enable-RT.patch
Patch579: 0279-powerpc-traps-Use-PREEMPT_RT.patch
Patch580: 0280-powerpc-pseries-iommu-Use-a-locallock-instead-local_.patch
Patch581: 0281-powerpc-kvm-Disable-in-kernel-MPIC-emulation-for-PRE.patch
Patch582: 0282-powerpc-stackprotector-work-around-stack-guard-init-.patch
Patch583: 0283-powerpc-Avoid-recursive-header-includes.patch
Patch584: 0284-POWERPC-Allow-to-enable-RT.patch
Patch585: 0285-drivers-block-zram-Replace-bit-spinlocks-with-rtmute.patch
Patch586: 0286-tpm_tis-fix-stall-after-iowrite-s.patch
Patch587: 0287-signals-Allow-rt-tasks-to-cache-one-sigqueue-struct.patch
Patch588: 0288-signal-Prevent-double-free-of-user-struct.patch
Patch589: 0289-genirq-Disable-irqpoll-on-rt.patch
Patch590: 0290-sysfs-Add-sys-kernel-realtime-entry.patch
Patch591: 0291-Add-localversion-for-RT-release.patch
Patch592: 0292-net-xfrm-Use-sequence-counter-with-associated-spinlo.patch
Patch593: 0293-sched-Fix-migration_cpu_stop-requeueing.patch
Patch594: 0294-sched-Simplify-migration_cpu_stop.patch
Patch595: 0295-sched-Collate-affine_move_task-stoppers.patch
Patch596: 0296-sched-Optimize-migration_cpu_stop.patch
Patch597: 0297-sched-Fix-affine_move_task-self-concurrency.patch
Patch598: 0298-sched-Simplify-set_affinity_pending-refcounts.patch
Patch599: 0299-sched-Don-t-defer-CPU-pick-to-migration_cpu_stop.patch
Patch600: 0300-printk-Enhance-the-condition-check-of-msleep-in-pr_f.patch
Patch601: 0301-locking-rwsem-rt-Remove-might_sleep-in-__up_read.patch
Patch602: 0302-mm-zsmalloc-Convert-zsmalloc_handle.lock-to-spinlock.patch
Patch603: 0303-sched-Fix-get_push_task-vs-migrate_disable.patch
Patch604: 0304-sched-Switch-wait_task_inactive-to-HRTIMER_MODE_REL_.patch
Patch605: 0305-preempt-Move-preempt_enable_no_resched-to-the-RT-blo.patch
Patch606: 0306-mm-Disable-NUMA_BALANCING_DEFAULT_ENABLED-and-TRANSP.patch
Patch607: 0307-fscache-Use-only-one-fscache_object_cong_wait.patch
Patch608: 0308-fscache-Use-only-one-fscache_object_cong_wait.patch
Patch609: 0309-locking-Drop-might_resched-from-might_sleep_no_state.patch
Patch610: 0310-drm-i915-gt-Queue-and-wait-for-the-irq_work-item.patch
Patch611: 0311-irq_work-Allow-irq_work_sync-to-sleep-if-irq_work-no.patch
Patch612: 0312-irq_work-Handle-some-irq_work-in-a-per-CPU-thread-on.patch
Patch613: 0313-irq_work-Also-rcuwait-for-IRQ_WORK_HARD_IRQ-on-PREEM.patch
Patch614: 0314-eventfd-Make-signal-recursion-protection-a-task-bit.patch
Patch615: 0315-stop_machine-Remove-this_cpu_ptr-from-print_stop_inf.patch
Patch616: 0316-aio-Fix-incorrect-usage-of-eventfd_signal_allowed.patch
Patch617: 0317-Linux-5.10.111-rt66-REBASE.patch
Patch618: 0318-rt-remove-extra-parameter-from-__trace_stack.patch
# Keep rt_version matched up with this patch.
Patch619: 0319-Linux-5.10.115-rt67-REBASE.patch

#Photon Specific Changes
Patch700: 0000-Revert-clockevents-Stop-unused-clockevent-devices.patch

# RT Runtime Greed
Patch701: 0001-RT-PATCH-sched-rt-RT_RUNTIME_GREED-sched-feature.patch
Patch702: use-kmsg_dump-iterator-for-RT.patch

# Patchset to conditional restart_tick upon idle_exit
# https://lore.kernel.org/lkml/162091184942.29796.4815200413212139734.tip-bot2@tip-bot2/
Patch703: 0001-tick-nohz-Evaluate-the-CPU-expression-after-the-stat.patch
Patch704: 0002-tick-nohz-Conditionally-restart-tick-on-idle-exit.patch
Patch705: 0003-tick-nohz-Remove-superflous-check-for-CONFIG_VIRT_CP.patch
Patch706: 0004-tick-nohz-Update-idle_exittime-on-actual-idle-exit.patch
Patch707: 0005-tick-nohz-Update-nohz_full-Kconfig-help.patch
Patch708: 0006-tick-nohz-Only-wakeup-a-single-target-cpu-when-kicki.patch
Patch709: 0007-tick-nohz-Change-signal-tick-dependency-to-wakeup-CP.patch
Patch710: 0008-tick-nohz-Kick-only-_queued_-task-whose-tick-depende.patch
Patch711: 0009-tick-nohz-Call-tick_nohz_task_switch-with-interrupts.patch
Patch712: 0010-MAINTAINERS-Add-myself-as-context-tracking-maintaine.patch

#Patch to enable nohz with idle=poll
Patch713: 0001-Allow-tick-sched-timer-to-be-turned-off-in-idle-poll.patch

# Disable md5 algorithm for sctp if fips is enabled.
Patch714: 0001-disable-md5-algorithm-for-sctp-if-fips-is-enabled.patch

# Crypto:
# Patch to add drbg_pr_ctr_aes256 test vectors to testmgr
Patch1000: crypto-testmgr-Add-drbg_pr_ctr_aes256-test-vectors.patch
# Patch to call drbg and dh crypto tests from tcrypt
Patch1001: tcrypt-disable-tests-that-are-not-enabled-in-photon.patch
Patch1002: 0001-Initialize-jitterentropy-before-ecdh.patch
Patch1003: 0002-FIPS-crypto-self-tests.patch
# Patch to remove urandom usage in rng module
Patch1004: 0001-FIPS-crypto-rng-Jitterentropy-RNG-as-the-only-RND-source.patch
# Patch to remove urandom usage in drbg and ecc modules
Patch1005: 0003-FIPS-crypto-drbg-Jitterentropy-RNG-as-the-only-RND.patch
#Patch to not make shash_no_setkey static
Patch1006: 0001-fips-Continue-to-export-shash_no_setkey.patch
%if 0%{?fips}
# FIPS canister usage patch
Patch1008: 0001-FIPS-canister-binary-usage.patch
Patch1009: 0001-scripts-kallsyms-Extra-kallsyms-parsing.patch
%else
%if 0%{?kat_build}
Patch1010: 0003-FIPS-broken-kattest.patch
%endif
%endif

#Patches for i40e driver
Patch1500: i40e-xdp-remove-XDP_QUERY_PROG-and-XDP_QUERY_PROG_HW-XDP-.patch
Patch1501: 0001-Add-support-for-gettimex64-interface.patch

#Patches for ice driver
Patch1510: 0001-ice-Use-PTP_SYS_OFFSET_EXTENDED_IOCTL-support.patch

#Patches for iavf driver
Patch1511: 0001-iavf-Use-PTP_SYS_OFFSET_EXTENDED_IOCTL-support.patch

#Patches for vmci driver
Patch1521:       001-return-correct-error-code.patch
Patch1522:       002-switch-to-kvfree_rcu-API.patch
Patch1523:       003-print-unexpanded-names-of-ioctl.patch
Patch1524:       004-enforce-queuepair-max-size-for-IOCTL_VMCI_QUEUEPAIR_ALLOC.patch
Patch1531:       0001-whitespace-formatting-change-for-vmci-register-defines.patch
Patch1532:       0002-add-MMIO-access-to-registers.patch
Patch1533:       0003-detect-DMA-datagram-capability.patch
Patch1534:       0004-set-OS-page-size.patch
Patch1535:       0005-register-dummy-IRQ-handlers-for-DMA-datagrams.patch
Patch1536:       0006-allocate-send-receive-buffers-for-DMAdatagrams.patch
Patch1537:       0007-add-support-for-DMA-datagrams-send.patch
Patch1538:       0008-add-support-for-DMA-datagrams-receive.patch
Patch1539:       0009-fix-the-description-of-vmci_check_host_caps.patch
Patch1540:       0010-no-need-to-clear-memory-after-dma_alloc_coherent.patch
Patch1541:       0011-fix-error-handling-paths-in-vmci_guest_probe_device.patch
Patch1542:       0012-check-exclusive-vectors-when-freeing-interrupt1.patch
Patch1543:       0013-release-notification-bitmap-inn-error-path.patch
Patch1544:       0014-add-support-for-arm64.patch

BuildArch:      x86_64

BuildRequires:  bc
BuildRequires:  kbd
BuildRequires:  kmod-devel
BuildRequires:  glib-devel
BuildRequires:  xerces-c-devel
BuildRequires:  xml-security-c-devel
BuildRequires:  libdnet-devel
BuildRequires:  libmspack-devel
BuildRequires:  Linux-PAM-devel
BuildRequires:  openssl-devel
BuildRequires:  procps-ng-devel
BuildRequires:  audit-devel
BuildRequires:  python3-macros

%if 0%{?fips}
BuildRequires: gdb
%endif

Requires:       kmod
Requires:       filesystem
Requires(pre): (coreutils or toybox)
Requires(preun): (coreutils or toybox)
Requires(post):(coreutils or toybox)
Requires(postun):(coreutils or toybox)

%description
The Linux package contains the Linux kernel with RT (real-time)
features.
%if 0%{?fips}
This kernel is FIPS certified.
%endif

%package devel
Summary:        Kernel Dev
Group:          System Environment/Kernel
Requires:       %{name} = %{version}-%{release}
Requires:       python3
Requires:       gawk
%description devel
The Linux package contains the Linux kernel dev files

%package docs
Summary:        Kernel docs
Group:          System Environment/Kernel
Requires:       python3
%description docs
The Linux package contains the Linux kernel doc files

%prep
# Using autosetup is not feasible
%setup -q -n linux-%{version}
%ifarch x86_64
# Using autosetup is not feasible
%setup -q -T -D -b 6 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 7 -n linux-%{version}
# Using autosetup is not feasible
%setup -q -T -D -b 8 -n linux-%{version}
%endif
%if 0%{?fips}
# Using autosetup is not feasible
%setup -q -T -D -b 16 -n linux-%{version}
%endif

%autopatch -p1 -m0 -M20

#VMW
%autopatch -p1 -m55 -M57

# CVE
%autopatch -p1 -m100 -M107

# RT
%autopatch -p1 -m301 -M714

%autopatch -p1 -m1000 -M1006

%if 0%{?fips}
%autopatch -p1 -m1008 -M1009
%else
%if 0%{?kat_build}
%patch1010 -p1
%endif
%endif

#Patches for i40e driver
pushd ../i40e-%{i40e_version}
%autopatch -p1 -m1500 -M1501
popd

#Patches for ice driver
pushd ../ice-%{ice_version}
%patch1510 -p1
popd

#Patches for iavf driver
pushd ../iavf-%{iavf_version}
%patch1511 -p1
popd

# vmci
%patch1521 -p1
%patch1522 -p1
%patch1523 -p1
%patch1524 -p1
%patch1531 -p1
%patch1532 -p1
%patch1533 -p1
%patch1534 -p1
%patch1535 -p1
%patch1536 -p1
%patch1537 -p1
%patch1538 -p1
%patch1539 -p1
%patch1540 -p1
%patch1541 -p1
%patch1542 -p1
%patch1543 -p1
%patch1544 -p1

%build
make %{?_smp_mflags} mrproper

%ifarch x86_64
cp %{SOURCE1} .config
arch="x86_64"
%endif
%if 0%{?fips}
cp ../fips-canister-%{fips_canister_version}/fips_canister.o crypto/
cp ../fips-canister-%{fips_canister_version}/fips_canister_wrapper.c crypto/
# Change m to y for modules that are in the canister
%include %{SOURCE17}
cp %{SOURCE18} crypto/
%else
%if 0%{?kat_build}
# Change m to y for modules in katbuild
%include %{SOURCE17}
%endif
%endif

sed -i 's/CONFIG_LOCALVERSION="-rt"/CONFIG_LOCALVERSION="-%{release}-rt"/' .config

%if 0%{?kat_build}
sed -i '/CONFIG_CRYPTO_SELF_TEST=y/a CONFIG_CRYPTO_BROKEN_KAT=y' .config
%endif

%include %{SOURCE5}

make %{?_smp_mflags} V=1 KBUILD_BUILD_VERSION="1-photon" \
    KBUILD_BUILD_HOST="photon" ARCH=${arch} %{?_smp_mflags}

%if 0%{?fips}
%include %{SOURCE9}
%endif

%ifarch x86_64

# build i40e module
bldroot="${PWD}"
pushd ../i40e-%{i40e_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} clean
make %{?_smp_mflags} -C src KSRC=${bldroot} %{?_smp_mflags}
popd

# build iavf module
pushd ../iavf-%{iavf_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} clean
make %{?_smp_mflags} -C src KSRC=${bldroot} %{?_smp_mflags}
popd

# build ice module
pushd ../ice-%{ice_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} clean
make %{?_smp_mflags} -C src KSRC=${bldroot} %{?_smp_mflags}
popd
%endif

%define __modules_install_post \
for MODULE in $(find %{buildroot}%{_modulesdir} -name *.ko); do \
  ./scripts/sign-file sha512 certs/signing_key.pem certs/signing_key.x509 $MODULE \
  rm -f $MODULE.{sig,dig} \
  xz $MODULE \
done \
%{nil}

# We want to compress modules after stripping. Extra step is added to
# the default __spec_install_post.
%define __spec_install_post\
%{?__debug_package:%{__debug_install_post}}\
%{__arch_install_post}\
%{__os_install_post}\
%{__modules_install_post}\
%{nil}

%install
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vdm 755 %{buildroot}/boot
install -vdm 755 %{buildroot}%{_docdir}/%{name}-%{uname_r}
install -vdm 755 %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}
install -vdm 755 %{buildroot}%{_libdir}/debug/%{_modulesdir}
make %{?_smp_mflags} INSTALL_MOD_PATH=%{buildroot} modules_install

%ifarch x86_64

# install i40e module
bldroot="${PWD}"
pushd ../i40e-%{i40e_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install
popd

# install iavf module
pushd ../iavf-%{iavf_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install
popd

# install ice module
pushd ../ice-%{ice_version}
make %{?_smp_mflags} -C src KSRC=${bldroot} INSTALL_MOD_PATH=%{buildroot} \
    INSTALL_MOD_DIR=extra MANDIR=%{_mandir} modules_install mandocs_install
popd

# Verify for build-id match
# We observe different IDs sometimes
# TODO: debug it
ID1=$(readelf -n vmlinux | grep "Build ID")
./scripts/extract-vmlinux arch/x86/boot/bzImage > extracted-vmlinux
ID2=$(readelf -n extracted-vmlinux | grep "Build ID")
if [ "$ID1" != "$ID2" ] ; then
  echo "Build IDs do not match"
  echo $ID1
  echo $ID2
  exit 1
fi
install -vm 644 arch/x86/boot/bzImage %{buildroot}/boot/vmlinuz-%{uname_r}
%endif

# Restrict the permission on System.map-X file
install -vm 400 System.map %{buildroot}/boot/System.map-%{uname_r}
install -vm 644 .config %{buildroot}/boot/config-%{uname_r}
cp -r Documentation/* %{buildroot}%{_docdir}/%{name}-%{uname_r}

%if 0%{?__debug_package}
install -vm 644 vmlinux %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux-%{uname_r}
# `perf test vmlinux` needs it
ln -s vmlinux-%{uname_r} %{buildroot}%{_libdir}/debug/%{_modulesdir}/vmlinux
%endif

cat > %{buildroot}/boot/%{name}-%{uname_r}.cfg << "EOF"
# GRUB Environment Block
photon_cmdline=init=/lib/systemd/systemd ro loglevel=3 quiet nosoftlockup intel_idle.max_cstate=0 mce=ignore_ce nowatchdog cpuidle.off=1 nmi_watchdog=0 audit=0
photon_linux=vmlinuz-%{uname_r}
photon_initrd=initrd.img-%{uname_r}
EOF

# Register myself to initramfs
mkdir -p %{buildroot}%{_localstatedir}/lib/initramfs/kernel
cat > %{buildroot}%{_localstatedir}/lib/initramfs/kernel/%{uname_r} << "EOF"
--add-drivers "cn dm-mod megaraid_sas"
EOF

# Cleanup dangling symlinks
rm -rf %{buildroot}%{_modulesdir}/source \
       %{buildroot}%{_modulesdir}/build

find . -name Makefile* -o -name Kconfig* -o -name *.pl | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy
find arch/%{archdir}/include include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy
find $(find arch/%{archdir} -name include -o -name scripts -type d) -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy
find arch/%{archdir}/include Module.symvers include scripts -type f | xargs sh -c 'cp --parents "$@" %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}' copy
%ifarch x86_64
# CONFIG_STACK_VALIDATION=y requires objtool to build external modules
install -vsm 755 tools/objtool/objtool %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}/tools/objtool/
install -vsm 755 tools/objtool/fixdep %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r}/tools/objtool/
%endif

cp .config %{buildroot}%{_usrsrc}/%{name}-headers-%{uname_r} # copy .config manually to be where it's expected to be
ln -sf "%{_usrsrc}/%{name}-headers-%{uname_r}" "%{buildroot}%{_modulesdir}/build"
find %{buildroot}/lib/modules -name '*.ko' -print0 | xargs -0 chmod u+x

%include %{SOURCE2}
%include %{SOURCE4}

%post
/sbin/depmod -a %{uname_r}
ln -sf %{name}-%{uname_r}.cfg /boot/photon.cfg

%files
%defattr(-,root,root)
/boot/System.map-%{uname_r}
/boot/config-%{uname_r}
/boot/vmlinuz-%{uname_r}
%config(noreplace) /boot/%{name}-%{uname_r}.cfg
%config %{_localstatedir}/lib/initramfs/kernel/%{uname_r}
%defattr(0644,root,root)
%{_modulesdir}/*
%exclude %{_modulesdir}/build
%{_sysconfdir}/modprobe.d/iavf.conf
# ICE driver firmware files are packaged in linux-firmware
%exclude /lib/firmware/updates/intel/ice

%files docs
%defattr(-,root,root)
%{_defaultdocdir}/%{name}-%{uname_r}/*
%{_mandir}/*

%files devel
%defattr(-,root,root)
%{_modulesdir}/build
%{_usrsrc}/%{name}-headers-%{uname_r}

%changelog
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-10
- .config: enable CONFIG_NET_ACT_SIMP
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-9
- Enable cgroup v1 stats
- .config: enable PERCPU_STATS
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-8
- Avoid TSC recalibration
* Fri Jul 15 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-7
- Enable config options needed to build N3000 FPGA driver.
* Wed Jul 13 2022 Srinidhi Rao <srinidhir@vmware.com> 5.10.118-6
- Fix for CVE-2022-21505
* Tue Jul 12 2022 Keerthana K <keerthanak@vmware.com> 5.10.118-5
- Reduce FIPS canister memory footprint by disabling CONFIG_KALLSYMS_ALL
- Add only fips_canister-kallsyms to vmlinux instead of all symbols
* Fri Jul 01 2022 Harinadh D <hdommaraju@vmware.com> 5.10.118-4
- VMCI patches & configs
* Fri Jun 24 2022 Shreenidhi Shedi <sshedi@vmware.com> 5.10.118-3
- Fix debug_package macro usage while adding vmlinux to debuginfo rpm
* Wed Jun 15 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 5.10.118-2
- Enable config_livepatch
* Mon Jun 13 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.118-1
- Update to version 5.10.118
* Wed Jun 01 2022 Ajay Kaher <akaher@vmware.com> 5.10.109-4
- Fix for CVE-2022-1966, CVE-2022-1972
* Mon May 23 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.109-3
- Fix for CVE-2022-21499
* Thu May 12 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.109-2
- Fix for CVE-2022-29582
* Fri Apr 29 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.109-1
- Update to version 5.10.109
* Tue Apr 05 2022 Alexey Makhalov <amakhalov@vmware.com> 5.10.103-4
- .config: enable zstd compression for squashfs.
- .config: enable crypto user api rng.
- .config: enable CONFIG_EXT2_FS_XATTR
* Mon Mar 21 2022 Ajay Kaher <akaher@vmware.com> 5.10.103-3
- Fix for CVE-2022-1016
* Mon Mar 14 2022 Bo Gan <ganb@vmware.com> 5.10.103-2
- Fix SEV and Hypercall alternative inst. patches
* Tue Mar 08 2022 srinidhira0 <srinidhir@vmware.com> 5.10.103-1
- Update to version 5.10.103
* Wed Feb 09 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.93-5
- Fix for CVE-2022-0435
* Sat Feb 05 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.93-4
- Fix for CVE-2022-0492
* Tue Jan 25 2022 Sharan Turlapati <sturlapati@vmware.com> 5.10.93-3
- Fix for CVE-2022-22942
* Tue Jan 25 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-2
- Fix CVE-2022-0330
* Fri Jan 21 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.93-1
- Update to version 5.10.93
* Sat Jan 08 2022 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.83-7
- Fix CVE-2021-4155 and CVE-2021-4204
* Mon Dec 20 2021 Keerthana K <keerthanak@vmware.com> 5.10.83-6
- crypto_self_test and broken kattest module enhancements
* Fri Dec 17 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.83-5
- mm: fix percpu alloacion for memoryless nodes
- pvscsi: fix disk detection issue
* Fri Dec 17 2021 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 5.10.83-4
- Disable md5 algorithm for sctp if fips is enabled.
* Tue Dec 14 2021 Harinadh D <hdommaraju@vmware.com> 5.10.83-3
- remove lvm in add-drivers list
- lvm drivers are built as part of dm-mod
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 5.10.83-2
- Bump up to compile with python 3.10
* Mon Dec 06 2021 srinidhira0 <srinidhir@vmware.com> 5.10.83-1
- Update to version 5.10.83
* Mon Nov 29 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.78-7
- Enable eBPF Net Packet filter support.
* Thu Nov 18 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.78-6
- Add vhost and vhost-net drivers in config
* Thu Nov 18 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.78-5
- Add PCI quirk to allow multiple devices under the same virtual
- PCI bridge to be put into separate IOMMU groups.
* Wed Nov 17 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.78-4
- Enable nohz for idle=poll
* Wed Nov 17 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.78-3
- Allow PCI resets disablement from vfio_pci
* Thu Nov 11 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 5.10.78-2
- compile with openssl 3.0.0
* Mon Nov 08 2021 Vikash Bansal <bvikas@vmware.com> 5.10.78-1
- Update to version 5.10.78
* Tue Oct 26 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.75-1
- Update to version 5.10.75
* Thu Sep 09 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.61-2
- .config enable CONFIG_MOUSE_PS2_VMMOUSE and CONFIG_INPUT_UINPUT
- Enable sta by default
* Fri Aug 27 2021 Ankit Jain <ankitja@vmware.com> 5.10.61-1
- Update to version 5.10.61
* Wed Aug 18 2021 Keerthana K <keerthanak@vmware.com> 5.10.52-2
- Update ice driver to v1.6.4
- Update i40e driver to v2.15.9
- Update iavf driver to v4.2.7
* Fri Jul 23 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.52-1
- Update to version 5.10.52
* Thu Jul 15 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.46-2
- Fix for CVE-2021-33909
* Mon Jun 28 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.46-1
- Update to version 5.10.46
* Thu Jun 24 2021 Ankit Jain <ankitja@vmware.com> 5.10.42-4
- Conditional tick_restart upon idle_exit
* Tue Jun 22 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.42-3
- Fix for CVE-2021-3609
* Thu Jun 10 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-2
- Added script to check structure compatibility between fips_canister.o and vmlinux.
* Thu Jun 03 2021 Keerthana K <keerthanak@vmware.com> 5.10.42-1
- Update to version 5.10.42
- Remove XR usb driver support
- .config: Enable CONFIG_FANOTIFY_ACCESS_PERMISSIONS
* Wed Jun 02 2021 Keerthana K <keerthanak@vmware.com> 5.10.35-3
- Fix for CVE-2021-3573
* Thu May 20 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-2
- Fix for CVE-2021-3564
* Mon May 17 2021 Ajay Kaher <akaher@vmware.com> 5.10.35-1
- Update to version 5.10.35
* Thu May 13 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-10
- Fix for CVE-2021-23133
* Tue May 11 2021 Ankit Jain <ankitja@vmware.com> 5.10.25-9
- .config: Enable INFINIBAND, MLX5_INFINIBAND
* Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-8
- Fix CVE-2020-26147, CVE-2020-24587, CVE-2020-24586, CVE-2020-24588,
- CVE-2020-26145, CVE-2020-26141
* Tue May 11 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.25-7
- Fix CVE-2021-3489, CVE-2021-3490, CVE-2021-3491
* Tue May 04 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-6
- Remove buf_info from device accessible structures in vmxnet3
* Thu Apr 29 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.25-5
- Update canister binary.
- use jent by drbg and ecc.
- Enable hmac(sha224) self test and broket KAT test.
* Thu Apr 22 2021 Keerthana K <keerthanak@vmware.com> 5.10.25-4
- Remove hmac(sha224) from broken kat test.
* Mon Apr 19 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.25-3
- Fix for CVE-2021-23133
* Thu Apr 15 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.25-2
- Fix for CVE-2021-29154
* Mon Mar 22 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.25-1
- Update to version 5.10.25
* Sun Mar 21 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.21-3
- Do not execute some tests twice
- Support future disablement of des3
- Do verbose build
- Canister update.
* Wed Mar 17 2021 Srinidhi Rao <srinidhir@vmware.com> 5.10.21-2
- Use jitterentropy rng instead of urandom in rng module.
* Tue Mar 16 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.21-1
- Update to version 5.10.21
* Mon Mar 01 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-10
- FIPS canister update
* Thu Feb 18 2021 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.10.4-9
- Fix /boot/photon.cfg symlink when /boot is a separate partition.
* Thu Feb 18 2021 Sharan Turlapati <sturlapati@vmware.com> 5.10.4-8
- Enable CONFIG_IFB
* Wed Feb 17 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-7
- Added latest out of tree version of Intel ice driver
* Wed Feb 17 2021 Vikash Bansal <bvikas@vmware.com> 5.10.4-6
- Added support for RT RUNTIME GREED
* Mon Feb 15 2021 Keerthana K <keerthanak@vmware.com> 5.10.4-5
- Added crypto_self_test and kattest module.
- These patches are applied when kat_build is enabled.
* Wed Feb 03 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.4-4
- Update i40e driver to v2.13.10
- Add out of tree iavf driver
- Enable CONFIG_NET_TEAM
* Wed Jan 27 2021 Alexey Makhalov <amakhalov@vmware.com> 5.10.4-3
- Build kernel with FIPS canister.
* Mon Jan 25 2021 Ankit Jain <ankitja@vmware.com> 5.10.4-2
- Enabled CONFIG_WIREGUARD
* Mon Jan 11 2021 Him Kalyan Bordoloi <bordoloih@vmware.com> 5.10.4-1
- Update to version 5.10.4
* Tue Nov 10 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-4
- Fix CVE-2020-8694
* Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 5.9.0-3
- Fix CVE-2020-25704
* Tue Oct 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-2
- Revert d254087 (clockevents: Stop unused clockevent devices)
- Solve cyclictest regression introduced in 4.1
* Tue Oct 27 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-1
- Update to version 5.9.0
* Tue Oct 06 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 5.9.0-rc7.1
- Update to version 5.9.0-rc7
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.19.127-2
- openssl 1.1.1
* Tue Jun 23 2020 Keerthana K <keerthanak@vmware.com> 4.19.127-1
- Update to version 4.19.127
* Tue Jun 16 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.115-10
- Add latest out of tree version of i40e driver
* Wed Jun 10 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.115-9
- Enable CONFIG_VFIO_NOIOMMU
* Fri Jun 05 2020 Ankit Jain <ankitja@vmware.com> 4.19.115-8
- Enabled CONFIG_BINFMT_MISC
* Tue Jun 02 2020 Vikash Bansal <bvikas@vmware.com> 4.19.115-7
- Add patch to fix CVE-2019-18885
* Fri May 29 2020 Shreenidhi Shedi <sshedi@vmware.com> 4.19.115-6
- Keep modules of running kernel till next boot
* Fri May 22 2020 Tapas Kundu <tkundu@vmware.com> 4.19.115-5
- Deprecate linux-rt-tools in favor of linux-tools.
- Deprecate python3-perf in favor of linux-python3-perf.
* Thu May 21 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.115-4
- Add ICE network driver support in config
* Fri May 15 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.115-3
- Add uio_pic_generic driver support in config
* Wed May 06 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 4.19.115-2
- Add patch to fix CVE-2020-10711
* Wed May 06 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.115-1
- Upgrade to 4.19.115
* Wed Apr 29 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.98-5
- Enable additional config options.
* Mon Mar 23 2020 Alexey Makhalov <amakhalov@vmware.com> 4.19.98-4
- Fix perf compilation issue with binutils >= 2.34.
* Sun Mar 22 2020 Tapas Kundu <tkundu@vmware.com> 4.19.98-3
- Added python3-perf subpackage
* Tue Mar 17 2020 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.98-2
- Add tools subpackage to include perf, turbostat and cpupower.
- Update the last few perf python scripts in Linux kernel to use
- python3 syntax.
* Tue Jan 28 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.98-1
- Upgrade to 4.19.98
* Thu Jan 16 2020 Srinidhi Rao <srinidhir@vmware.com> 4.19.82-4
- Enable DRBG HASH and DRBG CTR support.
* Fri Jan 03 2020 Keerthana K <keerthanak@vmware.com> 4.19.82-3
- Remove FIPS patch that enables fips for algorithms which are not fips allowed.
* Thu Dec 12 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.19.82-2
- Fix patch that wont apply on 4.19.82. Revert when upgraded to 4.19.87 or more
* Tue Nov 12 2019 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.19.82-1
- Introduce a new kernel flavor 'linux-rt' supporting real-time (RT) features.
